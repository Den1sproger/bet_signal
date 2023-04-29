import pymysql

from .db_config import *



class Database:
    """The class responsible for working with the database of subscribes"""

    def connect_to_db(self):
        # Connect to the database
        # Подключение к базе данных
        connection = pymysql.connect(
            host=host, user=user, port=3306,
            password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection


    def get_all_table_elements(self, query: str, element: str) -> list[int | str]:
        connection = self.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

                data = cursor.fetchall()
                all_chat_id = [item[element] for item in data]

        return all_chat_id
    

    def get_users_full_data(self) -> dict[int, dict[str, list[str]]]:
        connection = self.connect_to_db()

        data = {}

        with connection:
            with connection.cursor() as cursor:
                insert_query = "SELECT id, nickname FROM subscribers;"
                cursor.execute(insert_query)

                for row in cursor.fetchall():
                    user_id = row['id']
                    insert_query = f"SELECT list_id FROM bundle WHERE user_id = {user_id};"
                    cursor.execute(insert_query)


                    mail_list = []
                    for i in cursor.fetchall():
                        list_id = i['list_id']
                        insert_query = f"SELECT list_name FROM mail_lists WHERE id = {list_id};"
                        cursor.execute(insert_query)

                        list_ = cursor.fetchall()[0]
                        mail_list.append(list_['list_name'])
                        
                    data[user_id] = {
                        row['nickname']: mail_list
                    }

        return data
    

    def get_chat_id_by_subscribes(self, subscribes: list[str]) -> list[int]:
        connection = self.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                
                subscribes = f'{subscribes}'.replace('[', '(').replace(']', ')')
                insert_query = f'SELECT id FROM mail_lists WHERE list_name IN {subscribes}'
                cursor.execute(insert_query)
                lists_id = [row['id'] for row in cursor.fetchall()]

                lists_id = f'{lists_id}'.replace('[', '(').replace(']', ')')
                insert_query = f'SELECT user_id FROM bundle WHERE list_id IN {lists_id}'
                cursor.execute(insert_query)
                users_id = [row['user_id'] for row in cursor.fetchall()]

                users_id = f'{users_id}'.replace('[', '(').replace(']', ')')
                insert_query = f'SELECT chat_id FROM subscribers WHERE id IN {users_id}'
                cursor.execute(insert_query)

                data = [int(row['chat_id']) for row in cursor.fetchall()]

        return data
    

    def get_one_data_cell(self, query: str, column: str = 'nickname') -> int | bool:
        connection = self.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

                row = cursor.fetchall()

        if row: return row[0][column]
        else: return False


    def action(self, query: str) -> None:
        connection = self.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(query)
                except pymysql.err.IntegrityError:
                    connection.rollback()
            connection.commit()


    def is_user_in_db(self, chat_id: str) -> bool:
        values = {0: False, 1: True}

        connection = self.connect_to_db()
        with connection:
            with connection.cursor() as cursor:
                insert_query = f"SELECT EXISTS(SELECT * FROM subscribers WHERE chat_id = '{chat_id}');"
                cursor.execute(insert_query)

                row = cursor.fetchall()[0]

        return values.get(row[insert_query[7:-1]])
    

    def is_maillist_in_user(self, user_id: int, mail_lists_id: list[int]) -> bool:
        connection = self.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                insert_query = f"SELECT list_id FROM bundle WHERE user_id = {user_id}"
                cursor.execute(insert_query)

                rows = cursor.fetchall()

        lists_id = [row['list_id'] for row in rows]
        intersection = list(set(mail_lists_id) & set(lists_id))

        if intersection: return True
        else: return False
        
    
    def __del__(self) -> int:
        # Destructor
        return 1