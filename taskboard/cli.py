import argparse
import json
import sys
from pathlib import Path
from taskboard import domain

def main():
    parser = argparse.ArgumentParser(description="Taskboard CLI")
    parser.add_argument('--database', type=str, default='tasks.sqlite3', help='Path to SQLite database')
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', type=str, help='Task title')

    list_parser = subparsers.add_parser('list', help='List all tasks')

    complete_parser = subparsers.add_parser('complete', help='Complete a task')
    complete_parser.add_argument('id', type=str, help='Task ID to complete')

    rename_parser = subparsers.add_parser('rename', help='Rename a task')
    rename_parser.add_argument('id', type=str, help='Task ID to rename')
    rename_parser.add_argument('title', type=str, help='New title for the task')

    args = parser.parse_args()
    db_path = args.database
    try:
        if args.command == 'add':
            result = domain.add_task(args.title, db_path)
            print(json.dumps(result), flush=True)
            sys.exit(0)
        elif args.command == 'list':
            result = domain.list_tasks(db_path)
            print(json.dumps(result), flush=True)
            sys.exit(0)
        elif args.command == 'complete':
            result = domain.complete_task(args.id, db_path)
            print(json.dumps(result), flush=True)
            sys.exit(0)
        elif args.command == 'rename':
            result = domain.rename_task(args.id, args.title, db_path)
            print(json.dumps(result), flush=True)
            sys.exit(0)
        else:
            parser.print_usage()
            sys.exit(1)
    except domain.TaskboardError as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr, flush=True)
        sys.exit(2)
    except Exception as e:
        print(json.dumps({'error': 'Internal error: ' + str(e)}), file=sys.stderr, flush=True)
        sys.exit(2)
