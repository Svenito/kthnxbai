# Set the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask.ext.script import Manager, Server
from app import app

manager = Manager(app)


@manager.command
def db_create():
    ''' Create the DB from scratch on specified server '''
    from migrate.versioning import api
    from app import db
    import os.path
    db.create_all()
    if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
        api.create(app.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
        api.version_control(app.config['SQLALCHEMY_DATABASE_URI'],
                            app.config['SQLALCHEMY_MIGRATE_REPO'])
    else:
        api.version_control(app.config['SQLALCHEMY_DATABASE_URI'],
                            app.config['SQLALCHEMY_MIGRATE_REPO'],
                            api.version(app.config['SQLALCHEMY_MIGRATE_REPO']))


@manager.command
def db_migrate():
    ''' Migrate the DB creating a new version '''
    import imp
    from migrate.versioning import api
    from app import db
    migration = (app.config['SQLALCHEMY_MIGRATE_REPO'] + '/versions/%03d_migration.py' %
                 (api.db_version(app.config['SQLALCHEMY_DATABASE_URI'],
                                 app.config['SQLALCHEMY_MIGRATE_REPO']) + 1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(app.config['SQLALCHEMY_DATABASE_URI'],
                                 app.config['SQLALCHEMY_MIGRATE_REPO'])
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(app.config['SQLALCHEMY_DATABASE_URI'],
                                              app.config['SQLALCHEMY_MIGRATE_REPO'],
                                              tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'])
    print 'New migration saved as ' + migration
    print 'Current database version: ' + str(api.db_version(
        app.config['SQLALCHEMY_DATABASE_URI'],
        app.config['SQLALCHEMY_MIGRATE_REPO']))


def check_animated(img):
    try:
        img.seek(1)
    except (EOFError):
        return 0
    return 1


@manager.command
def ingest_images():
    ''' This imports images from the to_process directory in the
    project root to the site. Generating thumbnails and entering
    details into the DB'''

    from PIL import Image as pimage
    import shutil
    from datetime import datetime
    from app import db
    from models import Image
    import subprocess

    max_width = 133.0
    max_height = 150.0

    src_path = os.path.join(os.path.dirname(__file__), 'to_process')
    files = os.listdir(src_path)
    valid_files = 'jpg jpeg gif png tiff'.split()

    for img_file in files:
        print('processing ' + img_file)
        try:
            filename, ext = img_file.split('.')
        except ValueError:
            print("Failed to get name and ext")
            continue
        if ext.lower() not in valid_files:
            print('Invalid extension for ' + img_file)
            continue

        img_filename = os.path.join(src_path, img_file)
        thumb_filename = os.path.join(src_path, (filename + '_thumb'))

        try:
            img = pimage.open(img_filename)
            width, height = img.size
            ratio = min(max_width / width, max_height / height)
            new_size = '%dx%d' % (int(width * ratio), int(height * ratio))

            convert_filename = img_filename
            is_animated = check_animated(img)
            if is_animated == 1:
                convert_filename = img_filename + '[0]'

            subprocess.call([app.config['PATH_TO_CONVERT'],
                             convert_filename, '-resize',
                             new_size, thumb_filename])
        except IOError:
            print('Unable to make thumb from ' + img_file)
            continue

        # write to DB
        db.session.close()
        new_image = Image(filename=filename, ext=ext,
                          added_on=datetime.utcnow(),
                          is_animated=is_animated)
        db.session.add(new_image)
        target_path = app.config['IMAGE_PATH']
        shutil.move(img_filename, target_path)
        thumb_target = os.path.join(target_path,
                                    os.path.basename(thumb_filename) + '.' + ext)
        shutil.copy(thumb_filename, thumb_target)
        os.remove(thumb_filename)
        db.session.commit()

    db.session.close()


# Turn on debugger
if app.config['DEBUG']:
    manager.add_command("runserver", Server(
                        use_debugger=True,
                        use_reloader=True,
                        host='0.0.0.0')
                        )
else:
    manager.add_command("runserver", Server(
                        use_debugger=False,
                        use_reloader=False,
                        host='0.0.0.0')
                        )

if __name__ == "__main__":
        manager.run()
