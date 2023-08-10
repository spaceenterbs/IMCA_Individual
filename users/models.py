from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    """
    User 모델 관리 클래스
    """

    use_in_migrations = True  # 마이그레이션에 UserManager에 포함하는 코드

    def create_user(
        self,
        login_id,
        email,
        password,
        nickname,
        profileImg,
        gender,
        name,
        **kwargs,
    ):
        if not email:
            raise ValueError("이메일은 필수사항입니다.")
        user = self.model(
            login_id=login_id,
            email=email,
            nickname=nickname,
            profileImg=profileImg,
            gender=gender,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)  # 기본 User 모델을 이용하여 저장하는 코드
        return user

    def create_superuser(
        self,
        login_id=None,
        email=None,
        password=None,
        nickname="IMCA",
        profileImg=None,
        gender="male",
        name="IMCA",
        **extra_fields,
    ):
        user = self.create_user(
            login_id=login_id,
            email=email,
            password=password,
            nickname=nickname,
            profileImg=profileImg,
            gender=gender,
            name=name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User 모델 + JWT
    """

    class GenderChoices(models.TextChoices):
        """
        성별 선택 모델 index[1]의 내용이 보여지는 값 index[0]의 내용이 실제 db에 저장되는 값
        """

        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    nickname = models.CharField(max_length=30, unique=True, null=False, blank=False)
    login_id = models.CharField(max_length=30, unique=True, null=False, blank=False)
    profileImg = models.ImageField(null=True, blank=True)
    email = models.CharField(max_length=30, unique=True, null=False, blank=False)
    gender = models.CharField(max_length=6, choices=GenderChoices.choices)
    name = models.CharField(max_length=10, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = "login_id"  # 로그인에 사용되는 필드입니당
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "user"
