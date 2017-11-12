# Import standard modules
import uuid
import logging

# Import local modules
import configuration
from .base import RequestBase


class RequestCommands(RequestBase):
    def __init__(self):
        """Class initialization"""
        RequestBase.__init__(self)
        self.valid_roles = ['admin', ]

    def serve(self):
        """Handle the request and serve the response"""
        RequestBase.serve(self)
        # Request values
        self.args = {}
        self.args['FORMAT'] = self.params.get_item('format')
        self.args['CONFIRM'] = self.params.get_item('confirm')
        self.args['DELETE'] = self.params.get_item('delete')
        self.args['UUID'] = self.params.get_item('uuid')
        self.args['NAME'] = self.params.get_utf8_item('name')
        self.args['DESCRIPTION'] = self.params.get_utf8_item('description')
        self.args['COMMAND'] = self.params.get_utf8_item('command')
        self.args['FOLDER'] = self.params.get_utf8_item('folder')
        self.args['PARAMETERS'] = self.params.get_utf8_item('parameters')
        self.args['SHELL'] = int(self.params.get_item('shell', 0))
        # Avoid empty description
        if not self.args['DESCRIPTION']:
            self.args['DESCRIPTION'] = self.args['NAME']
        # Response values
        self.values = {}
        self.values['ERRORS'] = []
        self.values['DATA'] = None
        existing_id = 0
        existing_name = ''
        existing_description = ''
        existing_command = ''
        existing_folder = ''
        existing_parameters = ''
        existing_shell = 0

        engine = self.open_settings_db()
        # The query configuration is valid when a format is not requested
        if not self.args['FORMAT']:
            # Get existing catalog details
            if self.args['UUID']:
                query_fields, query_data = engine.get_data(
                        'SELECT uuid, name, description, command, parameters, '
                        'folder, shell '
                        'FROM commands '
                        'WHERE uuid=?',
                        None,
                        (self.args['UUID'], ))
                if query_data:
                    if self.args['DELETE']:
                        # Delete existing command
                        logging.debug('Deleting tool: %s' % self.args['UUID'])
                        engine.execute('DELETE FROM commands WHERE uuid=?', (
                            self.args['UUID'], ))
                        engine.save()
                        logging.info('Deleted tool: %s' % self.args['UUID'])
                        # Reload empty page afer save
                        return 'REDIRECT:commands'
                    else:
                        (existing_id, existing_name, existing_description,
                         existing_command, existing_parameters, existing_folder,
                         existing_shell) = query_data[0]
            # Check the requested arguments for errors
            if self.args['CONFIRM']:
                # Check parameters for errors
                if not self.args['NAME']:
                    self.values['ERRORS'].append('Missing command name')
                if not self.args['COMMAND']:
                    self.values['ERRORS'].append('Missing command')
                # Process data
                if not self.values['ERRORS']:
                    if existing_id:
                        # Update existing command
                        logging.debug('Updating command: %s' %
                                      self.args['UUID'])
                        engine.execute('UPDATE commands '
                                       'SET name=?, description=?, command=?, '
                                       'parameters=?, folder=?, shell=? '
                                       'WHERE uuid=?', (
                                           self.args['NAME'],
                                           self.args['DESCRIPTION'],
                                           self.args['COMMAND'],
                                           self.args['PARAMETERS'],
                                           self.args['FOLDER'],
                                           self.args['SHELL'],
                                           self.args['UUID']))
                        logging.info('Updated command: %s' % self.args['UUID'])
                    else:
                        # Insert new command
                        logging.debug('Inserting command: %s' %
                                      self.args['NAME'])
                        engine.execute('INSERT INTO commands(uuid, name, '
                                       'description, command, parameters, '
                                       'folder, shell) '
                                       'VALUES(?, ?, ?, ?, ?, ?, ?)', (
                                           str(uuid.uuid4()),
                                           self.args['NAME'],
                                           self.args['DESCRIPTION'],
                                           self.args['COMMAND'],
                                           self.args['PARAMETERS'],
                                           self.args['FOLDER'],
                                           self.args['SHELL']))
                        logging.info('Inserted command: %s' % self.args['NAME'])
                    engine.save()
                    # Reload empty page afer save
                    return 'REDIRECT:commands'
            else:
                # Use existing details
                self.args['NAME'] = existing_name
                self.args['DESCRIPTION'] = existing_description
                self.args['COMMAND'] = existing_command
                self.args['PARAMETERS'] = existing_parameters
                self.args['SHELL'] = existing_shell
                self.args['FOLDER'] = existing_folder
        # Get existing folders list
        self.values['FIELDS'], self.values['FOLDERS'] = engine.get_data(
            'SELECT name, description FROM folders '
            'ORDER BY name')
        # Get existing commands list
        self.values['FIELDS'], self.values['DATA'] = engine.get_data(
            'SELECT commands.uuid, commands.folder, commands.name, '
            'commands.description, '
            'folders.visible, folders.description '
            'FROM commands '
            'LEFT JOIN folders '
            'ON folders.name=commands.folder '
            'ORDER BY commands.folder, commands.name')
        engine.close()
        if not self.args['FORMAT']:
            # Serve the commands page
            return self.get_template(
                'commands.tpl',
                ARGS=self.args,
                VALUES=self.values,
                printable_text_for_encoding=self.printable_text_for_encoding)
        elif self.args['FORMAT'] == 'json':
            # JSON format commands list
            results = []
            folder = {}
            for row in self.values['DATA']:
                # Add a new folder
                if folder.get('title') != row[1].encode('utf-8'):
                    commands = []
                    folder = {}
                    folder['title'] = row[1].encode('utf-8')
                    folder['folder'] = True
                    folder['expanded'] = True
                    folder['tooltip'] = row[5].encode('utf-8')
                    folder['children'] = commands
                    results.append(folder)
                # Add the command to the commands list object
                commands.append({
                    'title': '<a href="?uuid=%s">%s</a>' % (row[0], row[2]),
                    'tooltip': row[3].encode('utf-8'),
                    'key': row[0],
                })
            return results
        else:
            # Unexpected format
            return 'ABORT:500:Unexpected format: %s' % self.args['FORMAT']
