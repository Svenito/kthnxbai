from flask import Blueprint, request, session, render_template
from flask.ext.wtf import Form, SelectField, BooleanField
from flask.views import MethodView
from models import Image
from urlparse import urljoin

images = Blueprint('images', __name__, template_folder='templates')


class SortForm(Form):
    sort_by = SelectField(u'Sort by', choices=[('date_added', 'Date Added'),
                                               ('num_views', 'Num Views')])
    sort_order = SelectField(u'Sort order', choices=[('desc', 'Desc'),
                                                     ('asc', 'Asc')])
    num_per_page = SelectField(u'Num per page', choices=[('25', '25'),
                                                         ('50', '50'),
                                                         ('100', '100'),
                                                         ('999999999', 'All')])


class ListView(MethodView):
    def set_sorting(self):
        if request.form.get('sort_order'):
            session['sort_order'] = request.form.get('sort_order')

        if request.form.get('sort_by'):
            session['sort_by'] = request.form.get('sort_by')

        if request.form.get('num_per_page'):
            session['num_per_page'] = request.form.get('num_per_page')

    def get_context(self, pagenum):
        images = Image.get_sorted_list()

        try:
            num_per_page = session['num_per_page']
        except KeyError:
            num_per_page = 25
            session['num_per_page'] = num_per_page

        images = images.paginate(pagenum,
                                 int(num_per_page), False)

        form = SortForm(formdata=request.form)

        # reflect current setting in form
        try:
            form.sort_order.data = session['sort_order']
        except KeyError:
            pass

        try:
            form.sort_by.data = session['sort_by']
        except KeyError:
            pass

        try:
            form.num_per_page.data = session['num_per_page']
        except KeyError:
            pass

        context = {
            "images": images,
            "form": form
        }
        return context

    def get(self, pagenum):
        context = self.get_context(pagenum)
        return render_template('images/list.html', **context)

    def post(self, pagenum=1):
        self.set_sorting()
        context = self.get_context(pagenum)
        return render_template('images/gallery.html', **context)


class DetailView(MethodView):
    def get(self, filename):
        image = Image.query.filter_by(filename=filename).first_or_404()
        image.inc_num_views()
        return render_template('images/detail.html', image=image)


class RssView(MethodView):
    def make_external(self, url):
        return urljoin(request.url_root, 'static/images/' + url)

    def get(self):
        from werkzeug.contrib.atom import AtomFeed
        feed = AtomFeed('Recent Images',
                    feed_url=request.url, url=request.url_root)
        images = Image.query.order_by(Image.added_on.desc()) \
                      .limit(15).all()
        for image in images:
            feed.add(image.added_on,
                     unicode('<img src="'+self.make_external(image.filename + '.' + image.ext) + '">'),
                     content_type='html',
                     author='kthnxbai',
                     url=self.make_external(image.filename + '.' + image.ext),
                     updated=image.added_on
                     )
        return feed.get_response()


images.add_url_rule('/', view_func=ListView.as_view('list'),
                    defaults={'pagenum': 1})
images.add_url_rule('/<int:pagenum>/', view_func=ListView.as_view('list'))

images.add_url_rule('/reorder/<int:pagenum>/',
                    view_func=ListView.as_view('list'))
images.add_url_rule('/reorder/', view_func=ListView.as_view('list'))

images.add_url_rule('/detail/<filename>/',
                    view_func=DetailView.as_view('detail'))

images.add_url_rule('/latest.atom',
                    view_func=RssView.as_view('rss'))
