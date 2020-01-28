import os

from hdfs import Config, HdfsError


def catch_hdfs_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except HdfsError as e:
            print(e)
            return False
    return wrapper


class HadoopWebExplorer:
    def __init__(self, debug=False):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.hdfscli.cfg')
        self.client = Config(path).get_client()
        self.debug = debug

    def print(self, *args):
        if self.debug:
            print(*args)

    def path_exists(self, path):
        """
        Checks whether such path already exists
        :param path: path to check
        :type path: unicode
        :return: boolean flag indicating whether path already exists or not
        :rtype: bool
        """
        return self.client.status(path, strict=False) is not None

    @catch_hdfs_error
    def create_folder(self, folder_name):
        """
        Creates folder with the given name if it does not exist
        :param folder_name: the name of the folder we want to add
        :type folder_name: unicode
        :return: returns true if created folder or it already exists, otherwise false
        :rtype: bool
        """
        if self.path_exists(folder_name):
            print(f'Folder already exists: {folder_name}')
            return True

        self.print(f'Folder does not exist: {folder_name}')
        self.client.makedirs(folder_name)
        self.print(f'Folder created: {folder_name}')

    @catch_hdfs_error
    def write_to_file(self, folder_name, file_name, data, overwrite=False, append=False):
        """
        Writes provided data into file in the specified folder
        :param folder_name: name of the folder where file is located
        :type folder_name: unicode
        :param file_name: name of the file where data should be written to
        :type file_name: unicode
        :param data: data to be written
        :type data: unicode
        :param overwrite: overwrite any existing file or directory
        :type overwrite: bool
        :param append: append to a file rather than create a new one.
        :type append: bool
        :return: returns true if it successfully wrote the data, otherwise false
        :rtype: bool
        """
        path = os.path.join(folder_name, file_name)
        if append and not self.path_exists(path):
            self.client.write(path, data, encoding='utf-8', overwrite=overwrite)
        else:
            self.client.write(path, data, encoding='utf-8', overwrite=overwrite, append=append)
        self.print("Written data to HDFS file")

    @catch_hdfs_error
    def read_from_file(self, folder_name, file_name):
        """
        Reads from file in the specified folder
        :param folder_name: name of the folder where file is located
        :type folder_name: unicode
        :param file_name: name of the file where data should be read from
        :type file_name: unicode
        """
        path = os.path.join(folder_name, file_name)
        if not self.path_exists(path):
            self.print(f'File does not exists: {path}')
            return None
        return self.client.read(path)

    @catch_hdfs_error
    def delete_file(self, folder_name, file_name):
        """
        Deletes file in the specified folder
        :param folder_name: name of the folder where file is located
        :type folder_name: unicode
        :param file_name: name of the file to be deleted
        :type file_name: unicode
        :return: returns true if it successfully deleted the file, otherwise false
        :rtype: bool
        """
        path = os.path.join(folder_name, file_name)
        return self.client.delete(path)

    @catch_hdfs_error
    def delete_folder(self, folder_name):
        """
        Deletes the specified folder
        :param folder_name: name of the folder where file is located
        :type folder_name: unicode
        :return: returns true if it successfully deleted the folder, otherwise false
        :rtype: bool
        """
        return self.client.delete(folder_name, recursive=True)

    @catch_hdfs_error
    def explore_folder(self, folder_name):
        """
        Explores the specified folder
        :param folder_name: name of the folder to be observed
        :type folder_name: unicode
        """
        if not self.path_exists(folder_name):
            self.print(f'Folder does not exists: {folder_name}')
        self.print(f'Exploring folder: {folder_name}')
        for path, dirs, files in self.client.walk(folder_name, status=True):
            for file in files:
                block_size = file[1]['blockSize']
                size = file[1]['length']
                owner = file[1]['owner']
                self.print(f'\tFile: {file[0]}, blockSize: {block_size}, size: {size}, owner: {owner}')


# if __name__ == '__main__':
#     hadoop_explorer = HadoopWebExplorer()
#     hadoop_explorer.explore_folder('py_test_folder')
