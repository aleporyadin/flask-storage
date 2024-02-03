from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from app import db
from app.models import Post, Comment
from app.forms import PostForm, CommentForm

blog = Blueprint('blog', __name__)


@blog.route('/blog')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/blog.html', posts=posts)


@blog.route('/blog/add', methods=['GET', 'POST'])
def add_post():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, preview_image_url=form.preview_image_url.data,
                        author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog.index'))
    return render_template('blog/add_post.html', form=form)


@blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    found_post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, post=found_post, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('blog.post', post_id=found_post.id))
    comments = found_post.comments.order_by(Comment.timestamp.asc()).all()
    return render_template('blog/post.html', post=found_post, form=form, comments=comments)
