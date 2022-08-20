from BankAccountFileManager import BankAccountFileManager

"""CALL MANAGER"""


def call_bank_manager():
    with BankAccountFileManager() as manager:
        return manager.rename_files()


if __name__ == '__main__':
    call_bank_manager()
