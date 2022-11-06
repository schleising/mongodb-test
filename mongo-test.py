from __future__ import annotations
import sys
from typing import Optional
from mongoengine import connect, disconnect, Document, StringField, ReferenceField, EmailField, queryset_manager, QuerySet
from mongoengine.errors import ValidationError, NotUniqueError, DoesNotExist

class User(Document):
    email = EmailField(required=True, unique=True)

    firstName = StringField(max_length=50)
    lastName = StringField(max_length=50)

    @queryset_manager
    def GetByEmail(cls, queryset: QuerySet, email: str) -> User:
        try:
            user: User = queryset.get(email=email) # type: ignore
        except DoesNotExist:
            print('Creating New User')
            user = AddUser(email)

        return user

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField

def AddUser(email: Optional[str] = None) -> User:
    newUser = User()

    if email is not None:
        newUser.email = email
    else:
        newUser.email = input('Enter email address: ')
    newUser.firstName = input('Enter first name: ')
    newUser.lastName = input('Enter last name: ')
    newUser.save()

    return newUser

def AddPost() -> bool:
    newPost = TextPost()
    newPost.title = input('Enter Title: ')
    author = input('Enter Author Email: ')

    authorMatches = User.GetByEmail(author) # type: ignore

    newPost.author = authorMatches
    newPost.save()
    return True

def CloseConnectionAndExit() -> None:
    disconnect()
    sys.exit()

if __name__ == '__main__':

    print(connect('testdb'))

    while True:
        print()
        print('1: Add User')
        print('2: Add Post')
        print('3: List Users')
        print('4: List Posts')
        print('0: Clear Database')
        print('q: Quit')
        print()
        option = input('Select Option: ')
        print()

        try:
            match option.lower():
                case '1':
                    print('Adding User')
                    AddUser()
                case '2':
                    print('Adding Post')
                    if AddPost():
                        print('Post added')
                    else:
                        print('There was a problem')
                case '3':
                    print('Users')
                    for user in User.objects: # type: ignore
                        if isinstance(user, User):
                            print(f'Name: {user.firstName} {user.lastName} Email: {user.email}')
                case '4':
                    print('Posts')
                    for post in Post.objects: # type:ignore
                        if isinstance(post, Post) and isinstance(post.author, User):
                            print(f'User: {post.author.email} Title: {post.title}')
                case '0':
                    print('Clearing Database')
                    for user in User.objects: # type: ignore
                        if isinstance(user, User):
                            user.delete()
                    for post in Post.objects: # type: ignore
                        if isinstance(post, Post):
                            post.delete()
                case 'q':
                    print('Exiting')
                    CloseConnectionAndExit()
                case _:
                    print('Unknown Option')
        except ValidationError:
            print()
            print('Invalid Email Address')
        except NotUniqueError:
            print()
            print('Email Address not Unique')
        except DoesNotExist:
            print()
            print('Email Address does not Exist')
        except Exception as e:
            print('Error, exiting')
            print(type(e))
            print(e)
            CloseConnectionAndExit()
