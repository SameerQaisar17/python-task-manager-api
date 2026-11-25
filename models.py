from database import connect_db


class TaskManager:

    def create_task(self, title, description):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, description)
            VALUES (?, ?)
        """, (title, description))

        connection.commit()

        task_id = cursor.lastrowid

        connection.close()

        return self.get_task(task_id)

    def get_all_tasks(self, status=None):
        connection = connect_db()
        cursor = connection.cursor()

        if status:
            cursor.execute("""
                SELECT * FROM tasks
                WHERE status = ?
                ORDER BY id DESC
            """, (status,))
        else:
            cursor.execute("""
                SELECT * FROM tasks
                ORDER BY id DESC
            """)

        tasks = [dict(row) for row in cursor.fetchall()]

        connection.close()

        return tasks

    def get_task(self, task_id):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM tasks WHERE id = ?
        """, (task_id,))

        task = cursor.fetchone()

        connection.close()

        return dict(task) if task else None

    def update_task(self, task_id, title, description, status):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE tasks
            SET title = ?,
                description = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (title, description, status, task_id))

        connection.commit()

        connection.close()

        return self.get_task(task_id)

    def delete_task(self, task_id):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM tasks WHERE id = ?
        """, (task_id,))

        connection.commit()

        deleted = cursor.rowcount > 0

        connection.close()

        return deleted