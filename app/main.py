from flask import Blueprint , render_template , url_for , redirect , request
from flask_login import current_user
from .app import db
import datetime
from .models import User,Role,Book,UsersBook,Status

main = Blueprint('main',__name__)

@main.route('/')
def index():
    user = User
    role = Role
    userbooks = UsersBook
    book = Book
    books_list = Book.query.order_by(Book.id)


    return render_template('index.html', user=user,role=role,book=book,userbooks=userbooks, books_list=books_list)

@main.route('/issue')
def issue():
    user = User
    role = Role
    userbooks = UsersBook
    book = Book
    val = list()

    books_list = Book.query.order_by(Book.id)
    

    status=Status
    if current_user.is_authenticated:
        user_list = UsersBook.query.order_by(UsersBook.user)
        
    else:
        user_list = None 

    return render_template('Issue.html', check_val = val,user=user,role=role,book=book ,userbooks=userbooks,user_list=user_list, books_list=books_list,status=status)


@main.route('/add_book',methods=['POST','GET'])
def add_book():
    if request.method == "POST":

        name = request.form['new_name']
        year = request.form['new_year']
        author = request.form['new_author']
        val = request.form['new_val']
        check = Book.query.filter_by(name = name).first()


        if check:
            return render_template('index.html')
        
    
        new_book = Book(  name = name, year = year, author = author, quantity = val)

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('main.index'))

    else:
        return render_template('add.html')

@main.route('/add/<id>',methods=['POST','GET'])
def add(id):
    if request.method == "GET":
        
        new_user = current_user.id
        new_data = datetime.datetime.now()
        userbooks = UsersBook
        book = Book
        check_issue = userbooks.query.filter_by(user = new_user).first()
        bad_book = Book.query.filter_by(id = id).first()


        if bad_book.quantity <= 0:
            return redirect(url_for('main.index'))

        check_quantity = book.query.order_by(book.quantity).all()
        

        value = int(bad_book.quantity) - 1

        issue_status = 1
        new_book = id 

        rows = Book.query.filter_by(id = id).update({'quantity': value })

        new_issue = userbooks(date=new_data , user=new_user ,book=new_book,status=issue_status )

        db.session.add(new_issue)
        db.session.commit()
       
    return redirect(url_for('main.issue'))
    

@main.route('/delete/<id>',methods=['POST','GET'])
def delete(id):
    if request.method == "GET":
        userbooks = UsersBook
        new_user = current_user.id

        bad_appeal = userbooks.query.filter_by(id=id).first()

        bad_book = Book.query.filter_by(id = bad_appeal.book).first()


        value = int(bad_book.quantity) + 1

        db.session.delete(bad_appeal)
        rows = Book.query.filter_by(id = bad_book.id).update({'quantity': value })
        db.session.commit()

    return redirect(url_for('main.issue', userbooks=userbooks))    

@main.route('/delete_book/<id>',methods=['POST','GET'])
def delete_book(id):
    if request.method == "GET":
        userbooks = UsersBook
        new_user = current_user.id
        bad_appeal = Book.query.filter_by(id=id).first()
        if not bad_appeal:
            return redirect(url_for('main.issue'))
        db.session.delete(bad_appeal)
        db.session.commit()
    return redirect(url_for('main.issue', userbooks=userbooks))   


@main.route('/set/<id>',methods=['POST','GET'])
def set(id):
    if request.method == "POST":
        bad_book = Book.query.filter_by(id=id).first()

        new_id = id
        name = request.form['new_name']
        year = request.form['new_year']
        author = request.form['new_author']
        val = request.form['new_val']

        if not bad_book:
            red_book = Book.query.filter_by(id=id).first()
            return render_template('set.html', red_book = red_book)
        

        rows = Book.query.filter_by(id = id).update({'name': name })
        rows1 = Book.query.filter_by(id = id).update({'author': author })
        rows2 = Book.query.filter_by(id = id).update({'year': year })
        rows3 = Book.query.filter_by(id = id).update({'quantity': val })
        db.session.commit()
        return render_template('index.html')
        
    else:
        red_book = Book.query.filter_by(id=id).first()
        return render_template('set.html', red_book = red_book)


