Project Title = Online Quiz Platform (Website)

Project Feature:
    1: Smooth quiz experience
    2: Plagirism Proof Platform
    3: Quiz report for Students and Mentor
    4: Video proctered test
    5: More Upcoming features

Project Layout:

Setup:
    1: django-admins startproject assessment

    2: python manage.py startapp <appname>

    3: python manage.py runserver   -->   to active the server

    4: python manage.py createsuperuser
        enter username
        enter email
        enter password
            bypass for easy password if required (press y)
        

Routings:
    /   -->  /student   -->   Student dashboard

        /student/test   -->   To take test by test code
        /student/view_mentor   -->   To check all mentor list of whoom test is given
        /student/history   -->   To check all the history of test given
        /student/announcement   -->   To check all announcement by mentors
        /student/accept_community_rules   -->   (functonality endpoint) endpoint to accept the community rules
    
    /admin   -->   Platform admin to approve student

        /admin/approve/<int:user_id>   -->   (functonality endpoint) endpoint to approve the user profiles
        /admin/reject/<int:user_id>   -->   (functonality endpoint) endpoint to reject the user profiles
        /admin/mentor_invite   -->   Page to invite mentor via email

    /auth   -->   App to authenticate

        /auth/login   -->   page to login the user (student/mentor)
        /auth/register   -->   page to register user (student)
        /auth/verify_email   -->   page to verify the email of registered user
        /auth/logout   -->   (functonality endpoint) to logout the current logged user

    /mentor   -->   Mentor dashboard

        /mentor/info   -->   page to register
        /mentor/make_test_next
        /mentor/take_test
        /mentor/view_test
        /mentor/mentor_announcements
        /mentor/save_questions

    /livetestportal   -->   Portal for test/quiz
    /masteradmin   -->   Master Admin of platform