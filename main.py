"""Learn2Earn resource lending system (Python standard library only)."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name('learn2earn_data.json')


def starting_resources():
    return [
        {'id': 'R001', 'name': 'Laptop', 'category': 'Electronics', 'total': 10, 'available': 10},
        {'id': 'R002', 'name': 'Keyboard', 'category': 'Accessories', 'total': 5, 'available': 5},
        {'id': 'R003', 'name': 'Headset', 'category': 'Accessories', 'total': 3, 'available': 3},
    ]


fellows = {'F001': 'Ada', 'F002': 'John', 'F003': 'Grace'}
resources = starting_resources()
borrow_records = []


def list_resources():
    print('\nLEARN2EARN RESOURCE INVENTORY')
    print('--------------------------------')
    if not resources:
        print('No resources available.')
    for resource in resources:
        print(f"ID: {resource['id']} | Name: {resource['name']} | "
              f"Category: {resource['category']} | Total: {resource['total']} | "
              f"Available: {resource['available']}")


def find_resource(resource_id):
    resource_id = resource_id.strip().upper()
    for resource in resources:
        if resource['id'] == resource_id:
            return resource
    return None


def resource_exists(resource_id):
    return find_resource(resource_id) is not None


def add_resource(resource_id, name, category, total):
    resource_id, name, category = resource_id.strip().upper(), name.strip(), category.strip()
    if not resource_id or not name or not category:
        print('Error: ID, name and category are required.')
        return False
    if resource_exists(resource_id):
        print('Error: Resource ID already exists.')
        return False
    if type(total) is not int or total <= 0:
        print('Error: Total units must be a positive integer.')
        return False
    resources.append({'id': resource_id, 'name': name, 'category': category,
                      'total': total, 'available': total})
    print('Resource added successfully!')
    return True


def borrow_resource(fellow_id, resource_id, quantity):
    fellow_id, resource_id = fellow_id.strip().upper(), resource_id.strip().upper()
    if fellow_id not in fellows:
        print('Error: Fellow ID not found.')
        return False
    resource = find_resource(resource_id)
    if resource is None:
        print('Error: Resource ID not found.')
        return False
    if type(quantity) is not int or quantity <= 0:
        print('Error: Quantity must be a positive integer.')
        return False
    if quantity > resource['available']:
        print('Error: Not enough resources available.')
        return False
    borrow_records.append({'fellow_id': fellow_id, 'resource_id': resource_id,
                           'quantity': quantity})
    resource['available'] -= quantity
    print(f"Success: {fellows[fellow_id]} borrowed {quantity} {resource['name']}(s).")
    return True


def get_borrowed_quantity(fellow_id, resource_id):
    return sum(record['quantity'] for record in borrow_records
               if record['fellow_id'] == fellow_id.strip().upper()
               and record['resource_id'] == resource_id.strip().upper())


def return_resource(fellow_id, resource_id, quantity):
    fellow_id, resource_id = fellow_id.strip().upper(), resource_id.strip().upper()
    if fellow_id not in fellows:
        print('Error: Fellow ID not found.')
        return False
    resource = find_resource(resource_id)
    if resource is None:
        print('Error: Resource ID not found.')
        return False
    if type(quantity) is not int or quantity <= 0:
        print('Error: Quantity must be a positive integer.')
        return False
    if quantity > get_borrowed_quantity(fellow_id, resource_id):
        print('Error: You cannot return more than you borrowed.')
        return False
    remaining = quantity
    for record in borrow_records:
        if record['fellow_id'] == fellow_id and record['resource_id'] == resource_id:
            returned = min(remaining, record['quantity'])
            record['quantity'] -= returned
            remaining -= returned
            if remaining == 0:
                break
    borrow_records[:] = [record for record in borrow_records if record['quantity'] > 0]
    resource['available'] += quantity
    print(f"Success: {fellows[fellow_id]} returned {quantity} {resource['name']}(s).")
    return True


def search_resource(name):
    name = name.strip().lower()
    if not name:
        print('Error: Enter a resource name to search.')
        return
    matches = [resource for resource in resources if name in resource['name'].lower()]
    if not matches:
        print('No matching resource found.')
    for resource in matches:
        print(f"ID: {resource['id']} | Name: {resource['name']} | Available: {resource['available']}")


def filter_by_category(category):
    category = category.strip().lower()
    if not category:
        print('Error: Enter a category.')
        return
    matches = [resource for resource in resources if resource['category'].lower() == category]
    if not matches:
        print('No resources found in this category.')
    for resource in matches:
        print(f"ID: {resource['id']} | Name: {resource['name']} | "
              f"Category: {resource['category']} | Available: {resource['available']}")


def generate_report():
    total_units = sum(resource['total'] for resource in resources)
    available_units = sum(resource['available'] for resource in resources)
    print('\nLEARN2EARN INVENTORY REPORT')
    print('--------------------------------')
    print(f'Total Units: {total_units}')
    print(f'Available Units: {available_units}')
    print(f'Borrowed Units: {total_units - available_units}')
    print('\nLOW STOCK RESOURCES')
    low_stock = [resource for resource in resources if resource['available'] < 3]
    if not low_stock:
        print('No low-stock resources.')
    for resource in low_stock:
        print(f"{resource['name']} - {resource['available']} available")
    print('\nMOST BORROWED RESOURCES')
    most = max((resource['total'] - resource['available'] for resource in resources), default=0)
    if most == 0:
        print('No resources are currently borrowed.')
    else:
        for resource in resources:
            if resource['total'] - resource['available'] == most:
                print(f"{resource['name']} - {most} borrowed")


def view_borrow_records():
    print('\nOUTSTANDING BORROW RECORDS')
    if not borrow_records:
        print('No outstanding loans.')
    for record in borrow_records:
        print(f"Fellow: {record['fellow_id']} | Resource: {record['resource_id']} | "
              f"Quantity: {record['quantity']}")


def save_data():
    data = {'resources': resources, 'borrow_records': borrow_records}
    try:
        temporary_file = DATA_FILE.with_suffix('.tmp')
        temporary_file.write_text(json.dumps(data, indent=4), encoding='utf-8')
        temporary_file.replace(DATA_FILE)
        return True
    except OSError as error:
        print(f'Error: Could not save data: {error}')
        return False


def valid_saved_data(data):
    if not isinstance(data, dict):
        return False
    saved_resources, saved_records = data.get('resources'), data.get('borrow_records')
    if not isinstance(saved_resources, list) or not isinstance(saved_records, list):
        return False
    ids = set()
    for resource in saved_resources:
        if not isinstance(resource, dict) or not all(key in resource for key in ('id', 'name', 'category', 'total', 'available')):
            return False
        rid, name, category = resource['id'], resource['name'], resource['category']
        total, available = resource['total'], resource['available']
        if (not isinstance(rid, str) or not rid.strip() or rid != rid.strip().upper()
                or rid in ids or not isinstance(name, str) or not name.strip()
                or not isinstance(category, str) or not category.strip()
                or type(total) is not int or total <= 0 or type(available) is not int
                or not 0 <= available <= total):
            return False
        ids.add(rid)
    borrowed_by_resource = {rid: 0 for rid in ids}
    for record in saved_records:
        if not isinstance(record, dict) or not all(key in record for key in ('fellow_id', 'resource_id', 'quantity')):
            return False
        if (record['fellow_id'] not in fellows or record['resource_id'] not in ids
                or type(record['quantity']) is not int or record['quantity'] <= 0):
            return False
        borrowed_by_resource[record['resource_id']] += record['quantity']
    return all(resource['total'] - resource['available'] == borrowed_by_resource[resource['id']]
               for resource in saved_resources)


def load_data():
    if not DATA_FILE.exists():
        return
    try:
        data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
        if not valid_saved_data(data):
            print('Warning: Saved data is invalid; starting with default inventory.')
            return
        resources[:] = data['resources']
        borrow_records[:] = data['borrow_records']
        print('Saved inventory and loans loaded successfully.')
    except (OSError, ValueError, TypeError):
        print('Warning: Could not read saved data; starting with default inventory.')


def read_positive_integer(prompt):
    try:
        value = int(input(prompt))
        if value <= 0:
            print('Error: Enter a positive integer.')
            return None
        return value
    except ValueError:
        print('Error: Please enter a valid whole number.')
        return None


def run_demonstration():
    """Run the seven required tests on fresh data, then restore the user's state."""
    original_resources = [resource.copy() for resource in resources]
    original_records = [record.copy() for record in borrow_records]
    try:
        resources[:] = starting_resources()
        borrow_records.clear()
        print('\nREQUIRED DEMONSTRATION (ISOLATED TEST DATA)')
        print('\nTEST 1: ADA BORROWS 2 LAPTOPS')
        borrow_resource('F001', 'R001', 2)
        print('Available laptops:', find_resource('R001')['available'])
        print('\nTEST 2: JOHN BORROWS 3 KEYBOARDS')
        borrow_resource('F002', 'R002', 3)
        print('Available keyboards:', find_resource('R002')['available'])
        print('\nTEST 3: ADA RETURNS 1 LAPTOP')
        return_resource('F001', 'R001', 1)
        print('Available laptops:', find_resource('R001')['available'])
        print('\nTEST 4: GRACE REQUESTS 4 HEADSETS')
        borrow_resource('F003', 'R003', 4)
        print('Available headsets:', find_resource('R003')['available'])
        print('\nTEST 5: JOHN TRIES TO RETURN 4 KEYBOARDS')
        return_resource('F002', 'R002', 4)
        print('Available keyboards:', find_resource('R002')['available'])
        print('\nTEST 6: SEARCH FOR LAPtop')
        search_resource('LAPtop')
        print('\nTEST 7: FINAL REPORT')
        generate_report()
        view_borrow_records()
    finally:
        resources[:] = original_resources
        borrow_records[:] = original_records
        print('\nDemonstration complete. Your working inventory is unchanged.')


def main_menu():
    while True:
        print('\n================================')
        print('LEARN2EARN RESOURCE MANAGEMENT')
        print('================================')
        print('1. List Resources')
        print('2. Add Resource')
        print('3. Borrow Resource')
        print('4. Return Resource')
        print('5. Search Resource')
        print('6. Filter by Category')
        print('7. Generate Report')
        print('8. View Borrow Records')
        print('9. Run Required Demonstration')
        print('0. Exit')
        choice = input('\nEnter your choice: ').strip()
        if choice == '1':
            list_resources()
        elif choice == '2':
            resource_id = input('Resource ID: ')
            name = input('Resource name: ')
            category = input('Category: ')
            total = read_positive_integer('Total units: ')
            if total is not None and add_resource(resource_id, name, category, total):
                save_data()
        elif choice == '3':
            fellow_id = input('Fellow ID: ')
            resource_id = input('Resource ID: ')
            quantity = read_positive_integer('Quantity to borrow: ')
            if quantity is not None and borrow_resource(fellow_id, resource_id, quantity):
                save_data()
        elif choice == '4':
            fellow_id = input('Fellow ID: ')
            resource_id = input('Resource ID: ')
            quantity = read_positive_integer('Quantity to return: ')
            if quantity is not None and return_resource(fellow_id, resource_id, quantity):
                save_data()
        elif choice == '5':
            search_resource(input('Search resource name: '))
        elif choice == '6':
            filter_by_category(input('Enter category: '))
        elif choice == '7':
            generate_report()
        elif choice == '8':
            view_borrow_records()
        elif choice == '9':
            run_demonstration()
        elif choice == '0':
            print('Thank you for using Learn2Earn.')
            break
        else:
            print('Error: Invalid menu choice.')


if __name__ == '__main__':
    load_data()
    try:
        main_menu()
    except (EOFError, KeyboardInterrupt):
        print('\nProgram closed.')