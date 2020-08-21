from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def show_menu():
    print("\n1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


def get_weekday(nr):
    if nr == 0:
        return "Monday"
    elif nr == 1:
        return "Tuesday"
    elif nr == 2:
        return "Wednesday"
    elif nr == 3:
        return "Thursday"
    elif nr == 4:
        return "Friday"
    elif nr == 5:
        return "Saturday"
    elif nr == 6:
        return "Sunday"


def add_days(days_added):
    date = datetime.today() + timedelta(days=days_added)
    return date.strftime('%d %b')


def show_day_tasks(task_rows, date):
    bullet_point, tasks = 1, 0
    for row in task_rows:
        if row.deadline.strftime('%d %b') == date:
            print(f"{bullet_point}. {row.task}")
            bullet_point += 1
            tasks += 1
    if tasks == 0:
        print("Nothing to do!")


program_running = True

while program_running:
    show_menu()
    choice = input()

    if choice == '1':
        rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            bullet_point = 1
            for row in rows:
                print(f"{bullet_point}. {row.task}")
                bullet_point += 1
    elif choice == '2':
        rows = session.query(Table).all()
        # Print each day of the week and its tasks
        current_weekday = datetime.today().weekday()
        day_count = 0
        w_day_count = 0
        for i in range(7):
            if (current_weekday + w_day_count) < 7:
                print(f"\n{get_weekday(current_weekday+w_day_count)} {add_days(day_count)}:")
            else:
                w_day_count = -current_weekday
                print(f"\n{get_weekday(current_weekday + w_day_count)} {add_days(day_count)}:")
            bullet_point, tasks = 1, 0
            show_day_tasks(rows, add_days(day_count))
            day_count += 1
            w_day_count += 1
    elif choice == '3':
        rows = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        bullet_point = 1
        for row in rows:
            print(f"{bullet_point}. {row.task}. {row.deadline.strftime('%d %b')}")
            bullet_point += 1
    elif choice == '4':
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print("Missed tasks:")
        bullet_point = 1
        for row in rows:
            print(f"{bullet_point}. {row.task}. {row.deadline.strftime('%d %b')}")
            bullet_point += 1
    elif choice == '5':
        print("Enter task")
        task_input = input()
        print("Enter deadline")
        deadline_input = input()
        new_row = Table(task=task_input, deadline=datetime.strptime(deadline_input, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif choice == '6':
        print("Choose the number of the task you want to delete:")
        rows = session.query(Table).order_by(Table.deadline).all()
        bullet_point = 1
        for row in rows:
            print(f"{bullet_point}. {row.task}. {row.deadline.strftime('%d %b')}")
            bullet_point += 1
        del_choice = int(input())
        session.delete(rows[del_choice - 1])
        session.commit()
        print("The task has been deleted!")
    elif choice == '0':
        program_running = False
