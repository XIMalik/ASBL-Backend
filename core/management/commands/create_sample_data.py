from django.core.management.base import BaseCommand
from core.models import Profile, Program, Person, ProgramPerson, News
from admissions.models import Application, AdminRequest


class Command(BaseCommand):
    help = 'Create comprehensive dummy data for all tables'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        AdminRequest.objects.all().delete()
        Application.objects.all().delete()
        ProgramPerson.objects.all().delete()
        News.objects.all().delete()
        Person.objects.all().delete()
        Program.objects.all().delete()
        Profile.objects.all().delete()

        # Create profiles
        profiles = [
            Profile.objects.create(email='admin@school.edu', role='admin'),
            Profile.objects.create(email='reviewer1@school.edu', role='reviewer'),
            Profile.objects.create(email='reviewer2@school.edu', role='reviewer'),
            Profile.objects.create(email='user1@example.com', role='user'),
            Profile.objects.create(email='user2@example.com', role='user'),
            Profile.objects.create(email='user3@example.com', role='user'),
        ]

        # Create programs
        programs = [
            Program.objects.create(
                name='Computer Science', description='Advanced CS program with AI focus',
                duration='4 years', level='Advanced', category='Technology', students=150,
                key_topics=['Python', 'Machine Learning', 'Data Structures', 'Algorithms'],
                additional_details='Includes industry internships'
            ),
            Program.objects.create(
                name='Business Administration', description='Comprehensive business program',
                duration='2 years', level='Intermediate', category='Business', students=200,
                key_topics=['Management', 'Finance', 'Marketing', 'Strategy']
            ),
            Program.objects.create(
                name='Data Science', description='Modern data analytics program',
                duration='18 months', level='Advanced', category='Technology', students=80,
                key_topics=['Statistics', 'Python', 'SQL', 'Visualization']
            ),
            Program.objects.create(
                name='Digital Marketing', description='Online marketing specialization',
                duration='1 year', level='Beginner', category='Marketing', students=120,
                key_topics=['SEO', 'Social Media', 'Analytics', 'Content Strategy']
            ),
        ]

        # Create people
        people = [
            Person.objects.create(
                name='Dr. Sarah Chen', position='CS Department Head', type='faculty',
                bio='Leading AI researcher with 15 years experience', email='s.chen@school.edu',
                achievements=['PhD MIT', '100+ Publications', 'AI Excellence Award'],
                specialties=['Machine Learning', 'Neural Networks', 'Computer Vision']
            ),
            Person.objects.create(
                name='Prof. Michael Rodriguez', position='Business Professor', type='faculty',
                bio='Former Fortune 500 executive turned educator', email='m.rodriguez@school.edu',
                achievements=['MBA Wharton', 'Former VP at Google', 'Best Teacher Award'],
                specialties=['Strategic Management', 'Innovation', 'Leadership']
            ),
            Person.objects.create(
                name='Dr. Emily Watson', position='Data Science Lead', type='faculty',
                bio='Statistics expert with industry consulting background', email='e.watson@school.edu',
                achievements=['PhD Statistics', 'Netflix Data Scientist', 'Kaggle Master'],
                specialties=['Statistical Modeling', 'Big Data', 'Predictive Analytics']
            ),
            Person.objects.create(
                name='James Park', position='Industry Mentor', type='mentor',
                bio='Senior software engineer at tech startup', email='j.park@techcorp.com',
                achievements=['10+ years experience', 'Tech Lead at 3 startups'],
                specialties=['Full Stack Development', 'System Design', 'Agile']
            ),
            Person.objects.create(
                name='Lisa Thompson', position='Career Advisor', type='staff',
                bio='Helping students navigate career paths', email='l.thompson@school.edu',
                achievements=['Career Counseling Certification', '500+ students placed'],
                specialties=['Resume Writing', 'Interview Prep', 'Networking']
            ),
        ]

        # Create program-person associations
        associations = [
            ProgramPerson.objects.create(program=programs[0], person=people[0]),
            ProgramPerson.objects.create(program=programs[0], person=people[3]),
            ProgramPerson.objects.create(program=programs[1], person=people[1]),
            ProgramPerson.objects.create(program=programs[2], person=people[2]),
            ProgramPerson.objects.create(program=programs[2], person=people[0]),
            ProgramPerson.objects.create(program=programs[3], person=people[1]),
        ]

        # Create news articles
        news_articles = [
            News.objects.create(
                title='New AI Lab Opens on Campus', excerpt='State-of-the-art facility for AI research',
                content='Our new artificial intelligence laboratory features cutting-edge GPU clusters...',
                category='Facilities', author=people[0], featured=True
            ),
            News.objects.create(
                title='Student Wins National Coding Competition', excerpt='CS student takes first place',
                content='Congratulations to our computer science student who won the national coding championship...',
                category='Achievements', author=people[4], featured=True
            ),
            News.objects.create(
                title='New Partnership with Tech Giants', excerpt='Industry collaboration announced',
                content='We are excited to announce partnerships with leading technology companies...',
                category='Partnerships', author=people[1], featured=False
            ),
            News.objects.create(
                title='Data Science Program Expansion', excerpt='New courses and faculty added',
                content='Due to high demand, we are expanding our data science program with new courses...',
                category='Programs', author=people[2], featured=True
            ),
        ]

        # Create applications
        applications = [
            Application.objects.create(
                first_name='Alice', last_name='Johnson', email='alice.j@email.com', phone='+1-555-0101',
                program=programs[0], personal_statement='Passionate about AI and machine learning...',
                goals='To develop innovative AI solutions for healthcare', status='pending',
                documents=['transcript.pdf', 'recommendation1.pdf'], identification_type='Passport'
            ),
            Application.objects.create(
                first_name='Bob', last_name='Smith', email='bob.smith@email.com', phone='+1-555-0102',
                program=programs[1], personal_statement='Experienced professional seeking MBA...',
                goals='To transition into executive leadership role', status='approved',
                documents=['resume.pdf', 'essays.pdf'], identification_type='Driver License'
            ),
            Application.objects.create(
                first_name='Carol', last_name='Davis', email='carol.d@email.com', phone='+1-555-0103',
                program=programs[2], personal_statement='Data enthusiast with strong math background...',
                goals='To become a senior data scientist', status='pending',
                documents=['portfolio.pdf'], identification_type='National ID'
            ),
            Application.objects.create(
                first_name='David', last_name='Wilson', email='david.w@email.com', phone='+1-555-0104',
                program=programs[0], personal_statement='Self-taught programmer looking to formalize education...',
                goals='To work at a top tech company', status='rejected',
                documents=['github_portfolio.pdf'], identification_type='Passport'
            ),
            Application.objects.create(
                first_name='Eva', last_name='Brown', email='eva.brown@email.com', phone='+1-555-0105',
                program=programs[3], personal_statement='Marketing professional seeking digital skills...',
                goals='To lead digital transformation initiatives', status='approved',
                documents=['certifications.pdf'], identification_type='Driver License'
            ),
        ]

        # Create admin requests
        admin_requests = [
            AdminRequest.objects.create(
                email='newadmin1@example.com', first_name='Frank', last_name='Miller',
                status='pending', user=profiles[3]
            ),
            AdminRequest.objects.create(
                email='newadmin2@example.com', first_name='Grace', last_name='Taylor',
                status='approved', user=profiles[4], reviewed_by=profiles[0]
            ),
            AdminRequest.objects.create(
                email='newadmin3@example.com', first_name='Henry', last_name='Anderson',
                status='rejected', user=profiles[5], reviewed_by=profiles[0]
            ),
        ]

        self.stdout.write(self.style.SUCCESS(f'Successfully created dummy data:'))
        self.stdout.write(f'- {len(profiles)} profiles')
        self.stdout.write(f'- {len(programs)} programs')
        self.stdout.write(f'- {len(people)} people')
        self.stdout.write(f'- {len(associations)} program-person associations')
        self.stdout.write(f'- {len(news_articles)} news articles')
        self.stdout.write(f'- {len(applications)} applications')
        self.stdout.write(f'- {len(admin_requests)} admin requests')