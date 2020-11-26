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
    books_list = Book.query.order_by(Book.id)
    status=Status
    
    

    if current_user.is_authenticated:
        user_list = UsersBook.query.order_by(UsersBook.user)
        
    else:
        user_list = None 

    return render_template('Issue.html', user=user,role=role,book=book ,userbooks=userbooks,user_list=user_list, books_list=books_list,status=status)


@main.route('/add/<id>',methods=['POST','GET'])
def add(id):
    if request.method == "GET":
        new_user = current_user.id
        new_data = datetime.datetime.now()
        userbooks = UsersBook
        book = Book
        check_issue = userbooks.query.filter_by(user = new_user).first()
        check_quantity = book.query.order_by(book.quantity).all()
        

        
        issue_status = 1
        new_book = id
        new_issue = userbooks(date=new_data , user=new_user ,book=new_book,status=issue_status )
    
        db.session.add(new_issue)
        db.session.commit()
        new_quantity = Book(date=new_data , user=new_user ,book=new_book,status=issue_status )
    
        db.session.add(new_issue)
        db.session.commit()
    return redirect(url_for('main.issue'))



@main.route('/delete/<id>',methods=['POST','GET'])
def delete(id):
    if request.method == "GET":
        userbooks = UsersBook
        new_user = current_user.id
        bad_appeal = userbooks.query.filter_by(id=id).first()
        if not bad_appeal:
            return redirect(url_for('main.issue'))
        db.session.delete(bad_appeal)
        db.session.commit()
    return redirect(url_for('main.issue'))    

@main.route('/set/<id>',methods=['POST','GET'])

def set(id):

    if request.method == 'POST':
        userbooks = UsersBook
        bad_issue= userbooks.query.filter_by(id=id).first()




        if not bad_issue:

            books_list = Books

            issue_list = Issue_log.query.order_by(Issue_log.date_log.desc())

            status_list = Status

            user = User

            role = Role

            error = "Изменения уже приступили в силу"

            return render_template('issue.html',books_list=books_list,issue_list=issue_list,status_list=status_list,user=user,role=role,error = error)







        new_date = bad_issue.date_log

        new_book = bad_issue.book_log




        user_id = request.form['new_user_issue']

        new_status = request.form['new_status']




        db.session.delete(bad_issue)

        new_issue = Issue_log(date_log=new_date , user_log=user_id ,book_log=new_book,status_log=new_status )

        db.session.add(new_issue)

        db.session.commit()

        return render_template('index.html')
    # else:
    #     book = Book.query.filter_by(id = id).first()
    #     issue = UsersBook
    #     status_list = Status.query.all()
    #     status = Status
    #     user = User
    #     user_list = User.query.all()
    #     role = Role
    #     return render_template('Issue.html',book=book,issue=issue,status_list=status_list,user=user,role=role,user_list=user_list)

    
