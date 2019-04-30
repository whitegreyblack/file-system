from tree import Tree
from models import DTO

def parse(dto, cache=None):
    response = DTO()
    for d in dto.data:
        try:
            tokenized_int = int(d.strip())
        except ValueError:
            if d == 'last' or d == 'x':
                response.data.extend(cache)
                cache = [] # make sure we cannot reuse
            response.messages.append(f"Error converting {d} to int")
        else:
            response.data.append(tokenized_int)
    response.success = bool(len(response.data))
    if not response.success:
        response.messages.append("No valid arguments parsed")
    return response

def main():
    """TODO: cache last result only"""
    data = None
    tree = Tree()
    while 1:
        action, *args = input('>>> ').split(' ')
        if action == 'exit':
            break
        elif action == 'last':
            if response.data:
                print(' '.join(str(d) for d in response.data))
            else:
                print("No data cached")
            continue
        valid_action = action in Tree.actions # make sure command is valid
        valid_method = hasattr(Tree, action) # make sure it's implemented
        if not (valid_action and valid_method):
            print("Command not found")
            continue
        command = getattr(tree, action)
        if args:
            request = DTO(data=args)
            response = parse(request, cache=data)
            if response.message:
                print(response.message)
            if not response.success:
                continue
            for x in response.data:
                response = command(x)
                if response.messages:
                    print(response.message)
        else:
            response = command()
            if response.messages:
                print(response.message) 
        if response.data:
            data = response.data
        else:
            data = None

if __name__ == "__main__":
    main()
