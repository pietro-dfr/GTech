import regex as re
import os 
from dataclasses import dataclass
#Classe Fields
class Fields:
    log = []

    name_pattern = re.compile(
        r"^(?:\p{Lu})(?:(?:')?(?:\p{Ll}))+(?:\-(?:\p{Lu})(?:(?:')?(?:\p{Ll}))+)*"
        r"(?: (?:(?:e|y|de(?: la| las| lo| los)?|do|dos|da|das|del|van|von|bin|le) )?"
        r"(?:(?:(?:d'|D'|O'|Mc|Mac|al\-))?(?:\p{Lu})(?:(?:')?(?:\p{Ll}))+|(?:\p{Lu})"
        r"(?:(?:')?(?:\p{Ll}))+"
        r"(?:\-(?:\p{Lu})(?:(?:')?(?:\p{Ll}))+)*))+(?: (?:Jr\.|II|III|IV))?$",
        flags=re.UNICODE
    )

    numeric_pattern = re.compile(r"\d{11}")

    @classmethod
    def is_valid_name(cls, name):
        if cls.name_pattern.fullmatch(name):
            return True
        cls.log.append("INVALID NAME!\n")
        return False

    @classmethod
    def is_valid_phone(cls, phone):
        if cls.numeric_pattern.fullmatch(phone):
            return True
        cls.log.append("INVALID PHONE!\n")
        return False

    @classmethod
    def is_valid_cpf(cls, cpf):
        if cls.numeric_pattern.fullmatch(cpf):
            return True
        cls.log.append("INVALID CPF!\n")
        return False

    @classmethod
    def all_valid(cls, name, cpf, phone):
        valid_name = cls.is_valid_name(name)
        valid_cpf = cls.is_valid_cpf(cpf)
        valid_phone = cls.is_valid_phone(phone)
        return valid_name and valid_cpf and valid_phone

    @classmethod
    def get_log(cls):
        return ''.join(cls.log)

    @classmethod
    def clear_log(cls):
        cls.log.clear()

#END

# ===== Classe Person =====
@dataclass
class Person:
    name: str
    cpf: str
    phone: str

#END
#Classe Registrations: 
class Registrations:
    MENU = (
        "=====================\n"
        "|      M E N U      |\n"
        "|-------------------|\n"
        "| [1]. Cadastrar    |\n"
        "| [2]. Excluir      |\n"
        "| [3]. Sair         |\n"
        "====================="
    )

    users: list[Person] = []

    @classmethod
    def add_user(cls, person: Person):
        cls.users.append(person)

    @classmethod
    def remove_user(cls, index: int):
        if 0 <= index < len(cls.users):
            cls.users.pop(index)

    @classmethod
    def already_registered(cls, cpf: str) -> bool:
        return any(user.cpf == cpf for user in cls.users)

#END
# ===== Main Program =====
def main():
    while True:
        print(Registrations.MENU)
        option_input = input("Escolha: ").strip()
        try:
            option = int(option_input)
            os.system("cls" if os.name == "nt" else "clear")
        except ValueError:
            print("Inválido!")
            continue

        if option == 1:
            name = input("NOME: ").strip()
            cpf = input("CPF: ").strip()
            phone = input("PHONE: ").strip()
            
            os.system("cls" if os.name == "nt" else "clear")
            
            if not Fields.all_valid(name, cpf, phone):
                print("CAMPOS INVÁLIDOS!")
                print(Fields.get_log())
                Fields.clear_log()
                continue

            if Registrations.already_registered(cpf):
                print("ALREADY REGISTERED!")
                continue

            Registrations.add_user(Person(name, cpf, phone))

        elif option == 2:
            if not Registrations.users:
                print("NÃO HÁ REGISTROS!")
                continue

            for i in range(len(Registrations.users)):
                print(f"{i} {Registrations.users[i].name}")
                
            try:
                remove_at = int(input("Digite o índice para remover: ").strip())
            except ValueError:
                print("DIGITE ALGO VÁLIDO!")
                continue

            if 0 <= remove_at < len(Registrations.users):
                Registrations.remove_user(remove_at)
            else:
                print("ÍNDICE INVÁLIDO!")

        elif option == 3:
            print("Tchau...")
            break
        else:
            print("Inválido!")
            

if __name__ == "__main__":
    main()
