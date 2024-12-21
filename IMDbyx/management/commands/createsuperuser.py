from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from IMDbyx.forms import CustomUserCreationForm

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        # Sobrescreve o comportamento do 'createsuperuser' para usar o CustomUserCreationForm
        form = CustomUserCreationForm(data=options)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()

            self.stdout.write(self.style.SUCCESS(f"Superuser {user.username} criado com sucesso"))
        else:
            # Caso o formulário não seja válido, exibe um erro
            raise CommandError('Erro ao criar superusuário. Verifique os campos.')
