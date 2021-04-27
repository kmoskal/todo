#!/usr/bin/env python3
import sys
import re

FILE_LOCATION = 'todo.txt'


class Todo:
    def __init__(self, file_location):
        self.file_location = file_location
        with open(self.file_location, 'r') as file:
            self.tasks_list = file.readlines()

    def help(self):
        ''' Display explanations of all commands '''
        print('help -> this screen')
        print('add -> add new task')
        print('ls -> display all of tasks')
        print('lsd -> display completed tasks')
        print('sort -> display sorted tasks by priority')
        print('show +project -> display tasks with +project or @person')
        print('done number -> mark task as done. Number of task in ls command')
        print('delete (number) -> delete tasks marked as done or number')

    def print_tasks_list(self, tasks_to_print, numbered=False):
        if numbered:
            i = 1
        else:
            i = ''
        for line in tasks_to_print:
            print(f'{i} {line}')
            if isinstance(i, int):
                i += 1

    def save(self, data,  mode='w'):
        with open(self.file_location, mode) as file:
            file.writelines(data)

    def done(self, task_number=None):
        ''' Mark task as done or undone. Add '-x' in front of the line
            or delete this mark if already exists.
        '''
        if task_number:
            try:
                for num in task_number:
                    if self.tasks_list[int(num)-1][:2] != '-x':
                        self.tasks_list[int(num)-1] = ('-x '
                                + self.tasks_list[int(num)-1])
                        print('Task marked as done:')
                        print(f'{self.tasks_list[int(num)-1]}')
                    else:
                        self.tasks_list[int(num)-1] = (
                                self.tasks_list[int(num)-1][3:])
                        print('Remove done mark:')
                        print(f'{self.tasks_list[int(num)-1]}')
            except IndexError:
                print(f'Task {num} not found.')
            self.save(self.tasks_list)
        # if user does not provide task number show all done tasks
        else:
            self.lsd()

    def delete_task(self, task_number=None):
        ''' Delete task/s marked as done if 'task_number' is empty list.
            Delete specific or all tasks from list task_number.
        '''
        updated_tasks_list = []
        any_change = False

        # if user specified numbers of tasks to delete
        if task_number:
            for i in range(len(self.tasks_list)):
                if str(i+1) not in task_number:
                    updated_tasks_list.append(self.tasks_list[i])
                else:
                    any_change = True
                    print(self.tasks_list[i])

            if any_change:
                answer = input('Press "y" if delete or "n" if not: ')
                if answer == 'y':
                    self.save(updated_tasks_list)
                    print(str(len(self.tasks_list)
                            - len(updated_tasks_list))
                            + ' tasks has been deleted.')
                elif answer == 'n':
                    print('Nothing has been deleted.')
                else:
                    print('Press "y" if yes or "n" if not!')

        # if user wants to delete all marked tasks
        else:
            for task in self.tasks_list:
                if task[:2] != '-x':
                    updated_tasks_list.append(task)
                else:
                    any_change = True
                    print(task)

            if any_change:
                answer = input('Press "y" if delete or "n" if not: ')
                if answer == 'y':
                    self.save(updated_tasks_list)
                    print(str(len(self.tasks_list)
                            - len(updated_tasks_list))
                            + ' tasks has been deleted.')
                elif answer == 'n':
                    print('Nothing has been deleted.')
                else:
                    print('Press "y" if yes or "n" if not!')

        if not any_change:
            print(f'Task/s number/s {task_number} not found')

    def add(self, args):
        ''' Add task to file '''
        string = []
        for i in range(len(args)-2):
            string.append(args[i+2])
        string = ' '.join(string)+'\n'
        print(f'New task: {string}')
        self.save(string, 'a')

    def sort(self):
        ''' Print sorted list of tasks by priority '{A}', '{B}'... '''
        priority_tasks = []
        for task in self.tasks_list:
            r1 = re.search(r'\{[A-Z]\}', task)
            if r1:
                priority_tasks.append(r1.group())
            else:
                priority_tasks.append('{a}')
        sorted_tasks = [priority for _, priority in sorted(zip(
                                priority_tasks, self.tasks_list))]
        self.print_tasks_list(sorted_tasks)

    def show(self, args=None):
        ''' Show tasks with special character e.g. @person or +project '''
        if args:
            tasks_list_to_show = []
            for arg in args:
                for task in self.tasks_list:
                    if arg in task:
                        tasks_list_to_show.append(task)
            if tasks_list_to_show:
                self.print_tasks_list(tasks_list_to_show)
        else:
            print('Enter a search arguments')

    def ls(self):
        ''' Print list of all tasks '''
        if self.tasks_list:
            self.print_tasks_list(self.tasks_list, numbered=True)
        else:
            print('There is nothing to do')

    def lsd(self):
        ''' Print completed tasks '''
        tasks_done = []
        for line in self.tasks_list:
            if line[:2] == '-x':
                tasks_done.append(line)
        if tasks_done:
            self.print_tasks_list(tasks_done)
        else:
            print('Nothing done yet')

    def check_command(self, args):
        if len(args) > 1:
            command = args[1]
            if command == 'add':
                self.add(args)
            elif command == 'ls':
                self.ls()
            elif command == 'lsd':
                self.lsd()
            elif command == 'done':
                self.done(args[2:])
            elif command == 'delete':
                self.delete_task(args[2:])
            elif command == 'sort':
                self.sort()
            elif command == 'show':
                self.show(args[2:])
            elif command == 'help':
                self.help()
            else:
                self.help()
        else:
            self.help()

def main():
    todo = Todo(FILE_LOCATION)
    todo.check_command(sys.argv)

if __name__ == '__main__':
    main()
