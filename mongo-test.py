import sys
from mongoengine import connect, disconnect, Document, StringField, ReferenceField, EmailField
from mongoengine.errors import ValidationError, NotUniqueError

class User(Document):
    email = EmailField(required=True, unique=True)

    firstName = StringField(max_length=50)
    lastName = StringField(max_length=50)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField

def AddUser() -> bool:
    newUser = User()
    newUser.email = input('Enter email address: ')
    newUser.firstName = input('Enter first name: ')
    newUser.lastName = input('Enter last name: ')
    newUser.save()

    return True

def AddPost() -> bool:
    newPost = TextPost()
    newPost.title = input('Enter Title: ')
    author = input('Enter Author Email: ')

    authorMatches = User.objects(email=author) # type: ignore

    if len(authorMatches) == 1:
        newPost.author = authorMatches[0]
        newPost.save()
        return True
    else:
        return False

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
                    if AddUser():
                        print('User added')
                    else:
                        print('There was a problem')
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
        except Exception as e:
            print('Error, exiting')
            print(type(e))
            print(e)
            CloseConnectionAndExit()
