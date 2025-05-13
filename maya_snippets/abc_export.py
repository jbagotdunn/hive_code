import maya.cmds as cmds
import os


# cmds.listRelatives(cmds.ls(sl=True)[0], ad=True, type="mesh") it will give
# you all the mssesh under your selection

class NoSaveFileException(Exception):
    pass


class NoObjectSelected(Exception):
    pass


def remove_digits_from_str(s):
    result = ''.join([i for i in s if not i.isdigit()])
    return result


def get_file_name():
    file_path = cmds.file(q=True, sn=True)
    if not file_path:
        raise NoSaveFileException('Please save the file before exporting abc')

    file_name = os.path.basename(file_path)
    raw_name, extension = os.path.splitext(file_name)
    raw_name = remove_digits_from_str(raw_name)
    node_name = cmds.ls(sl=True)[0]
    node_name = node_name.replace(':', '_')
    node_name = node_name.replace('|', '_')
    print('NODE ', node_name)
    raw_name = '{}{}.abc'.format(raw_name, node_name)

    return raw_name


def get_abc_save_name(project_dir, file_name):
    file_name = os.path.join('assets', file_name)
    full_name = os.path.join(project_dir, file_name)
    print(full_name)

    return full_name


def get_selection():
    objs = cmds.ls(sl=True)
    if not objs:
        raise NoObjectSelected('Please select an obj to export')
        print('nothing is selected')
    print(objs[0])
    return objs[0]


def export_selection_abc(obj, full_path):

    start_frame = str(cmds.playbackOptions(q=True, min=True))
    end_frame = str(cmds.playbackOptions(q=True, max=True))

    root = "-root {selection}".format(selection=obj)


    command = "-frameRange " + start_frame + " " + end_frame + \
              " -uvWrite -worldSpace " + root + \
              " -file " + full_path
    print(command)
    cmds.AbcExport(j=command)
    
    return True


def main():
    project_dir = cmds.workspace(q=True, rd=True)
    file_name = get_file_name()
    full_path = get_abc_save_name(project_dir, file_name)
    obj = get_selection()

    is_exported = export_selection_abc(obj=obj, full_path=full_path)
    if is_exported:
        print('EXPORTED: {fn} \nlocated {p}'.format(fn=file_name, p=full_path))


main()
file_name = get_file_name()

