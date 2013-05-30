import os
from flask import url_for, session
from app import app, db
from sqlalchemy import func
from random import randint


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    added_on = db.Column(db.DateTime)
    filename = db.Column(db.String(255), unique=True)
    ext = db.Column(db.String(4))
    num_views = db.Column(db.Integer, default=0)
    is_animated = db.Column(db.Integer, default=0)

    def thumbname(self):
        path = os.path.join(app.config['STATIC_URL'],
                            self.filename + "_thumb." + self.ext)
        return path

    def fullsize(self):
        path = os.path.join(app.config['STATIC_URL'],
                            self.filename + '.' + self.ext)
        return path

    def get_absolute_url(self):
        return url_for('image',
                       kwargs={"filename": self.filename + '.' + self.ext})

    def __unicode__(self):
        return self.filename + '.' + self.ext

    def get_random(self):
        max_id = db.session.query(func.max(Image.id)).first()[0]
        min_id = db.session.query(func.min(Image.id)).first()[0]

        rand_id = randint(min_id, max_id)
        while self.id == rand_id:
            rand_id = randint(min_id, max_id)

        return Image.query.filter_by(id=rand_id).first_or_404().filename

    def get_sorting(self):
        try:
            if session['sort_order']:
                sort_order = session['sort_order']
        except KeyError:
            sort_order = 'desc'

        try:
            if session['sort_by']:
                sort_by = session['sort_by']
        except KeyError:
            sort_by = 'date_added'
        return (sort_order, sort_by)

    @staticmethod
    def get_sorted_list():
        try:
            sort_order = session['sort_order']
        except KeyError:
            sort_order = 'desc'

        try:
            sort_by = session['sort_by']
        except KeyError:
            sort_by = 'date_added'

        images = Image.query
        if sort_order == 'asc':
            if sort_by == 'date_added':
                images = images.order_by(Image.added_on.asc())
            else:
                images = images.order_by(Image.num_views.asc())
            images = images.order_by(Image.id.asc())
        else:
            if sort_by == 'date_added':
                images = images.order_by(Image.added_on.desc())
            else:
                images = images.order_by(Image.num_views.desc())
            images = images.order_by(Image.id.desc())
        return images

    def next(self):
        sort_order, sort_by = self.get_sorting()

        if sort_order == 'asc':
            if sort_by == 'date_added':
                image = Image.query.\
                    filter(Image.added_on >= self.added_on).\
                    filter(Image.id != self.id).\
                    order_by(Image.added_on.asc(), Image.id.asc()).\
                    first()
            else:
                image = Image.query.\
                    filter(Image.num_views == self.num_views).\
                    filter(Image.id > self.id).first()
                if not image:
                    return Image.query.\
                        filter(Image.num_views > self.num_views).\
                        order_by(Image.num_views.asc(), Image.id.asc()).\
                        first()
        else:
            if sort_by == 'date_added':
                image = Image.query.\
                    filter(Image.added_on <= self.added_on).\
                    filter(Image.id != self.id).\
                    order_by(Image.added_on.desc(), Image.id.desc()).first()
            else:
                image = Image.query.\
                    filter(Image.num_views == self.num_views).\
                    filter(Image.id < self.id).\
                    order_by(Image.id.desc()).first()
                if not image:
                    return Image.query.\
                        filter(Image.num_views < self.num_views).\
                        order_by(Image.num_views.desc(), Image.id.desc()).\
                        first()

        return image

    def prev(self):
        sort_order, sort_by = self.get_sorting()

        if sort_order == 'asc':
            if sort_by == 'date_added':
                image = Image.query.\
                    filter(Image.added_on <= self.added_on).\
                    filter(Image.id != self.id).\
                    order_by(Image.added_on.desc(), Image.id.desc()).\
                    first()
            else:
                image = Image.query.filter(Image.num_views == self.num_views).\
                    filter(Image.id < self.id).order_by(Image.id.desc()).\
                    first()
                if not image:
                    return Image.query.\
                        filter(Image.num_views < self.num_views).\
                        order_by(Image.num_views.desc(), Image.id.desc()).\
                        first()
        else:
            if sort_by == 'date_added':
                image = Image.query.\
                    filter(Image.added_on >= self.added_on).\
                    filter(Image.id != self.id).\
                    order_by(Image.added_on.asc(), Image.id.asc()).\
                    first()
            else:
                image = Image.query.\
                    filter(Image.num_views == self.num_views).\
                    filter(Image.id > self.id).\
                    order_by(Image.id.asc()).\
                    first()
                if not image:
                    image = Image.query.\
                        order_by(Image.num_views.asc()).\
                        filter(Image.num_views > self.num_views).\
                        order_by(Image.num_views.asc(), Image.id.asc()).\
                        first()

        return image

    def inc_num_views(self):
        self.num_views += 1
        db.session.add(self)
        db.session.commit()
