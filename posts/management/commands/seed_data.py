import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from faker import Faker
from users.models import Profile
from posts.models import Post, Comment

fake = Faker()


class Command(BaseCommand):
    help = 'Seed database with fake users and posts for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=30,
            help='Number of posts to create (default: 30)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing data before seeding'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        num_posts = options['posts']
        clear = options['clear']

        if clear:
            self.stdout.write('🗑️  Clearing existing data...')
            Post.objects.all().delete()
            Comment.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✅ Cleared!'))

        # ── Create Users ──
        self.stdout.write(f'👤 Creating {num_users} users...')
        created_users = []

        for i in range(num_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"

            # Make sure username is unique
            while User.objects.filter(username=username).exists():
                username = f"{first_name.lower()}{random.randint(1, 9999)}"

            email = fake.email()
            while User.objects.filter(email=email).exists():
                email = fake.unique.email()

            user = User.objects.create_user(
                username=username,
                email=email,
                password='test1234',
                first_name=first_name,
                last_name=last_name,
            )

            # Update profile
            profile = user.profile
            profile.bio = fake.text(max_nb_chars=150)
            profile.location = fake.city()
            profile.website = fake.url() if random.random() > 0.5 else ''
            profile.save()

            created_users.append(user)
            self.stdout.write(f'   ✅ Created @{username}')

        # ── Create Follow Relationships ──
        self.stdout.write('🤝 Creating follow relationships...')
        all_users = list(User.objects.filter(is_superuser=False))

        for user in all_users:
            # Each user follows 3-7 random others
            others = [u for u in all_users if u != user]
            to_follow = random.sample(others, min(random.randint(3, 7), len(others)))
            for target in to_follow:
                user.profile.following.add(target.profile)

        self.stdout.write('   ✅ Follow relationships created!')

        # ── Create Posts ──
        self.stdout.write(f'📝 Creating {num_posts} posts...')

        post_templates = [
            "Just had the most amazing day! {}",
            "Thinking about {} lately. What do you all think?",
            "{}",
            "Hot take: {}",
            "Can't believe {}. Mind blown! 🤯",
            "Reminder that {}. Have a great day! 😊",
            "Anyone else feel like {}?",
            "Today I learned that {}. Pretty cool!",
            "{}! Who else agrees? 👇",
            "Real talk: {}",
        ]

        topics = [
            "the weather has been absolutely incredible",
            "learning new skills every day is so important",
            "kindness goes a long way in life",
            "technology is changing everything around us",
            "small steps lead to big achievements",
            "coffee is basically a personality at this point",
            "you should always chase your dreams",
            "the internet has made the world so small",
            "reading books is the best investment",
            "cooking at home saves so much money",
            "music has the power to change your mood instantly",
            "nature walks are the best therapy",
            "consistency is more important than perfection",
            "being kind costs nothing but means everything",
            "gratitude changes your entire perspective on life",
        ]

        created_posts = []
        for i in range(num_posts):
            user = random.choice(all_users)
            template = random.choice(post_templates)
            topic = random.choice(topics)
            content = template.format(topic)

            post = Post.objects.create(
                user=user,
                content=content,
            )
            created_posts.append(post)

        self.stdout.write('   ✅ Posts created!')

        # ── Create Likes ──
        self.stdout.write('❤️  Adding likes...')
        for post in created_posts:
            likers = random.sample(all_users, random.randint(0, min(8, len(all_users))))
            for liker in likers:
                post.likes.add(liker)

        self.stdout.write('   ✅ Likes added!')

        # ── Create Comments ──
        self.stdout.write('💬 Adding comments...')

        comment_templates = [
            "This is so true! 💯",
            "Totally agree with this!",
            "Never thought about it this way before.",
            "Thanks for sharing this!",
            "This made my day 😊",
            "So inspiring! Keep it up!",
            "100% facts right here.",
            "I needed to hear this today.",
            "This is amazing, thank you!",
            "Couldn't agree more!",
            "Wow, this is so relatable.",
            "Love this perspective!",
            "Great point! Sharing this.",
            "You always post the best stuff!",
            "Facts! 🔥",
        ]

        for post in created_posts:
            num_comments = random.randint(0, 5)
            commenters = random.sample(
                all_users,
                min(num_comments, len(all_users))
            )
            for commenter in commenters:
                Comment.objects.create(
                    post=post,
                    user=commenter,
                    content=random.choice(comment_templates)
                )

        self.stdout.write('   ✅ Comments added!')

        # ── Summary ──
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 45))
        self.stdout.write(self.style.SUCCESS('🎉 SEED COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('=' * 45))
        self.stdout.write(f'👤 Users created : {num_users}')
        self.stdout.write(f'📝 Posts created : {num_posts}')
        self.stdout.write(f'❤️  Likes added  : random')
        self.stdout.write(f'💬 Comments added: random')
        self.stdout.write('')
        self.stdout.write('🔑 All test users password: test1234')
        self.stdout.write(self.style.SUCCESS('=' * 45))