from django.views import View
from django.contrib import messages
import re
from django.views import View
from django.shortcuts import render, redirect
from .models import User,Book,Booking
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render



class FrontpageView(View):
    def get(self, request):
        return render(request, 'libraryapp/front_page.html')


class IndexView(View):
    def get(self, request):
        return render(request, 'libraryapp/index.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'libraryapp/about.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'libraryapp/contact.html')

class UserSignupView(View):
    def get(self, request):
        return render(request, 'libraryapp/user_signup.html')

    def post(self, request):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        age = request.POST.get('age')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        role ='user'

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or Email already exists")
            return redirect('user_signup')


        # validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect('user_signup')

        if not re.search(r'\d', password):
            messages.error(request, "Password must contain at least one digit")
            return redirect('user_signup')

        if not re.search(r'[A-Za-z]', password):
            messages.error(request, "Password must contain at least one letter")
            return redirect('user_signup')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, "Password must contain at least one special character")
            return redirect('user_signup')
            
        #Mobile number validation
        if not re.match(r'^\d{10}$', contact_no):
            messages.error(request, "Mobile number must be 10 digits long")
            return redirect('user_signup')


        user = User(first_name=first_name,last_name=last_name,username=username,password=password,age=age,address=address,contact_no=contact_no,email=email,role=role,is_approved=True )
        user.save()

        return redirect('index')


class LibrarianSignupView(View):
    def get(self, request):
        return render(request, 'libraryapp/librarian_signup.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        age = request.POST.get('age')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        role = 'librarian'
        library_name = request.POST.get('library_name')
        library_location = request.POST.get('library_location')
        library_image = request.FILES.get('library_image')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or Email already exists")
            return redirect('librarian_signup')


        #validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect('librarian_signup')

        if not re.search(r'\d', password):
            messages.error(request, "Password must contain at least one digit")
            return redirect('librarian_signup')

        if not re.search(r'[A-Za-z]', password):
            messages.error(request, "Password must contain at least one letter")
            return redirect('librarian_signup')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, "Password must contain at least one special character")
            return redirect('librarian_signup')

        
        librarian = User(first_name=first_name,last_name=last_name,username=username,password=password,age=age,address=address,contact_no=contact_no,email=email,library_name=library_name,role=role,library_location=library_location,library_image=library_image,is_approved=False)
        
        librarian.save()


       
        messages.success(request, "Your signup request has been sent for approval.")
        return redirect('index')


class LoginView(View):
    def get(self, request):
        return render(request, 'libraryapp/index.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username, password=password).first()

        if user is not None:
            request.session['user_id'] = user.id  
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'librarian':
                return redirect('librarian_dashboard')
            elif user.role == 'user':
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password")

        return render(request, 'libraryapp/index.html')

class LogoutView(View):
    def get(self, request):
        if 'user_id' in request.session:
            del request.session['user_id']
        return redirect('index')



class ApproveLibrarianView(View):
    def post(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('admin_dashboard')

        user = User.objects.filter(id=user_id, role='admin').first()
        if not user:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('admin_dashboard')

        librarian = User.objects.filter(pk=pk, role='librarian', is_approved=False).first()
        if librarian:
            librarian.is_approved = True
            librarian.save()
            # Send approval email
            send_mail(
                'Librarian Request Approved',
                'Congratulations! Your librarian request has been approved.',
                settings.EMAIL_HOST_USER,
                [librarian.email],
                fail_silently=False,
            )
            messages.success(request, "Librarian approved and email sent.")
        else:
            messages.error(request, "Invalid librarian ID or already approved.")
        
        return redirect('admin_dashboard')

class RejectLibrarianView(View):
    def post(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='admin').first()
        if not user:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('index')

        librarian = User.objects.filter(pk=pk, role='librarian', is_approved=False).first()
        if librarian:
            librarian.delete()
            # Send rejection email
            send_mail(
                'Librarian Request Rejected',
                'We regret to inform you that your librarian request has been rejected.',
                settings.EMAIL_HOST_USER,
                [librarian.email],
                fail_silently=False,
            )
            messages.success(request, "Librarian request rejected and email sent.")
        else:
            messages.error(request, "Invalid librarian ID or already approved.")
        
        return redirect('admin_dashboard')


class AdminDashboardView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='admin').first()
        if not user:
            messages.error(request, "You are not authorized to access this page.")
            return redirect('index')

        pending_librarians = User.objects.filter(role='librarian', is_approved=False)
        approved_librarians = User.objects.filter(role='librarian', is_approved=True)

        return render(request, 'libraryapp/admin_dashboard.html', {
            'pending_librarians': pending_librarians,
            'approved_librarians': approved_librarians
        })





class LibrarianDashboardView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        librarian = get_object_or_404(User, id=user_id, role='librarian', is_approved=True)

        # Retrieve library details
        library_details = {
            'name': librarian.library_name,
            'location': librarian.library_location,
            'image': librarian.library_image.url if librarian.library_image else None
        }

        # Retrieve books associated with this librarian
        books = Book.objects.filter(librarian=librarian)

        # Retrieve bookings associated with the librarian's library
        bookings = Booking.objects.filter(book__librarian=librarian).select_related('book', 'user')

        return render(request, 'libraryapp/librarian_dashboard.html', {
            'user': librarian,
            'library_details': library_details,
            'books': books,
            'bookings': bookings
        })


class DeleteApprovedLibraryView(View):
    def post(self, request, pk):
        # Check if the user is authenticated and has the 'admin' role
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='admin').first()
        if not user:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('index')

        librarian = User.objects.filter(pk=pk, role='librarian', is_approved=True).first()
        if librarian:
            librarian.delete()
            messages.success(request, "Approved library and librarian have been deleted.")
        else:
            messages.error(request, "Invalid librarian ID or not an approved librarian.")

        return redirect('admin_dashboard')


class UserDashboardView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='user').first()
        if not user:
            messages.error(request, "You are not authorized to access this page.")
            return redirect('index')

        # Retrieve the list of approved libraries
        approved_libraries = User.objects.filter(role='librarian', is_approved=True)

        return render(request, 'libraryapp/user_dashboard.html', {'approved_libraries': approved_libraries})



class LibraryDetailView(View):
    def get(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id).first()
        if not user:
            messages.error(request, "User not found or unauthorized.")
            return redirect('index')

        # librarian = get_object_or_404(User, pk=pk, role='librarian', is_approved=True)
        librarian=User.objects.filter(pk=pk,role='librarian', is_approved=True).first()
        books = Book.objects.filter(librarian=librarian)

        library_details = {
            'name': librarian.library_name,
            'location': librarian.library_location,
            'image': librarian.library_image.url if librarian.library_image else None,
            'librarian_name': librarian.username
        }

        return render(request, 'libraryapp/library_detail.html', {
            'library_details': library_details,
            'books': books
        })

    def post(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='user').first()
        if not user:
            messages.error(request, "You are not authorized to book books.")
            return redirect('index')

        # book = get_object_or_404(Book, pk=pk)
        book=Book.objects.filter(pk=pk).first()

        if book.is_booked:
            messages.error(request, 'This book is already booked.')
            return redirect('library_detail', pk=book.librarian.id)

        return redirect('booking_page', pk=pk)  # Redirect to booking page





class AddBookView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        librarian = User.objects.filter(id=user_id, role='librarian', is_approved=True).first()
        if not librarian:
            messages.error(request, "You are not authorized to add books.")
            return redirect('index')

        return render(request, 'libraryapp/add_book.html')

    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        librarian = User.objects.filter(id=user_id, role='librarian', is_approved=True).first()
        if not librarian:
            messages.error(request, "You are not authorized to add books.")
            return redirect('index')

        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        cover_image = request.FILES.get('cover_image')
        genre = request.POST.get('genre')
        language = request.POST.get('language')

        if not title or not author or not isbn or not genre or not language:
            messages.error(request, "All fields are required except cover image.")
            return render(request, 'libraryapp/add_book.html')


        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            cover_image=cover_image,
            genre=genre,
            language=language,
            librarian=librarian
        )

        book.save()
        messages.success(request, "Book added successfully.")
        return redirect('librarian_dashboard')




class EditBookView(View):
    def get(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        librarian = User.objects.filter(id=user_id, role='librarian', is_approved=True).first()
        if not librarian:
            messages.error(request, "You are not authorized to edit books.")
            return redirect('index')

        book = Book.objects.filter(pk=pk, librarian=librarian).first()
        if not book:
            messages.error(request, "Book not found or you are not authorized to edit this book.")
            return redirect('index')

        return render(request, 'libraryapp/edit_book.html', {'book': book})

    def post(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        librarian = User.objects.filter(id=user_id, role='librarian', is_approved=True).first()
        if not librarian:
            messages.error(request, "You are not authorized to edit books.")
            return redirect('index')

        book = Book.objects.filter(pk=pk, librarian=librarian).first()
        if not book:
            messages.error(request, "Book not found or you are not authorized to edit this book.")
            return redirect('index')

        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        cover_image = request.FILES.get('cover_image')
        genre = request.POST.get('genre')
        language = request.POST.get('language')

        if not title or not author or not isbn or not genre or not language:
            messages.error(request, "All fields are required except cover image.")
            return render(request, 'libraryapp/edit_book.html', {'book': book})

        # Update book details
        book.title = title
        book.author = author
        book.isbn = isbn
        book.genre = genre
        book.language = language
        if cover_image:
            book.cover_image = cover_image

        book.save()
        messages.success(request, "Book details updated successfully.")
        return redirect('librarian_dashboard')


class DeleteBookView(View):
    def post(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        librarian = User.objects.filter(id=user_id, role='librarian', is_approved=True).first()
        if not librarian:
            messages.error(request, "You are not authorized to delete books.")
            return redirect('index')

        book = Book.objects.filter(pk=pk, librarian=librarian).first()
        if not book:
            messages.error(request, "Book not found or you are not authorized to delete this book.")
            return redirect('librarian_dashboard')

        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('librarian_dashboard')


# # # # # # # # #Booking view

class BookingPageView(View):
    def get(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='user').first()
        if not user:
            messages.error(request, "You are not authorized to book books.")
            return redirect('index')

        # book = get_object_or_404(Book, pk=pk)
        book=Book.objects.filter(pk=pk).first()

        # Ensure book is available
        if book.is_booked:
            messages.error(request, 'This book is already booked.')
            return redirect('library_detail', pk=book.librarian.id)

        # Calculate return due date as 15 days from now
        return_due_date = datetime.now() + timedelta(days=15)

        return render(request, 'libraryapp/booking_page.html', {
            'book': book,
            'booked_on': datetime.now().date(),
            'return_due_date': return_due_date.date()
        })

    def post(self, request, pk):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='user').first()
        if not user:
            messages.error(request, "You are not authorized to book books.")
            return redirect('index')

        # book = get_object_or_404(Book, pk=pk)
        book=Book.objects.filter(pk=pk).first()

        if book.is_booked:
            messages.error(request, 'This book is already booked.')
            return redirect('library_detail', pk=book.librarian.id)

        # Calculate return due date as 15 days from now
        return_due_date = datetime.now() + timedelta(days=15)

        Booking.objects.create(
            book=book,
            user=user,
            booked_on=datetime.now().date(),
            return_due_date=return_due_date.date()
        )

        book.is_booked = True
        book.save()

        messages.success(request, 'Book booked successfully.')
        return redirect('library_detail', pk=book.librarian.id)


#Specified user bookings view

class UserProfileView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('index')

        user = User.objects.filter(id=user_id, role='user').first()
        if not user:
            messages.error(request, "You are not authorized to access this page.")
            return redirect('index')

        # Get the user's bookings
        bookings = Booking.objects.filter(user=user).select_related('book__librarian')

        return render(request, 'libraryapp/user_profile.html', {
            'user': user,
            'bookings': bookings
        })




