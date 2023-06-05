#!/usr/bin/python3
# contains the entry point of the command interpreter
import cmd
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """ contains instances and methods of this class """
    prompt = "(hbnb) "
    classes = {"BaseModel", "User", "State", "City", "Amenity", "Place",
               "Review"}

    def do_quit(self, args):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, args):
        """Exit the program"""
        return True

    def do_help(self, args):
        """Display help"""
        cmd.Cmd.do_help(self, args)

    def emptyline(self):
        """Do nothing for empty input"""
        pass

    def do_create(self, args):
        """Create a new instance of BaseModel"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = eval("{}()".format(class_name))

        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """Print the string representation of an instance"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instances = storage.all()
        instance_id = args[1]
        key = class_name + "." + instance_id

        if key not in instances:
            print("** no instance found **")
            return

        # Print the string representation of the instance
        print(instances[key])

    def do_destroy(self, args):
        """Delete an instance based on the class name and id"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instances = storage.all()
        instance_id = args[1]
        key = class_name + "." + instance_id

        if key not in instances:
            print("** no instance found **")
            return

        del instances[key]
        storage.save()

    def do_all(self, args):
        """Print all string representations of instances"""
        instances = storage.all()
        if not args:
            print([str(instance) for instance in instances.values()])
            return

        args = args.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        print([str(instance) for instance in instances
               .values() if type(instance).__name__ == class_name])

    def do_update(self, args):
        """Updates an instance based on the class name and id"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instances = storage.all()
        instance_id = args[1]
        key = class_name + "." + instance_id

        if key not in instances:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_name = args[2]
        attribute_value = args[3]

        instance = instances[key]
        setattr(instance, attribute_name, attribute_value)
        instance.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
