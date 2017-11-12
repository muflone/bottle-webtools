# Import standard modules
from collections import OrderedDict
import datetime
import shlex
import subprocess

# Import local modules
import configuration
from .base import RequestBase


class RequestRun(RequestBase):
    def __init__(self):
        """Class initialization"""
        RequestBase.__init__(self)
        self.login_required = False

    def serve(self):
        """Handle the request and serve the response"""
        RequestBase.serve(self)
        # Request values
        self.args = {}
        self.args['UUID'] = self.params.get_item('uuid')
        self.args['FORMAT'] = self.params.get_item('format')
        # Response values
        self.values = {}
        self.values['DESCRIPTION'] = None
        self.values['COMMAND'] = None
        self.values['SHELL'] = None
        self.values['ERRORS'] = []
        self.values['FIELDS'] = None
        self.values['STDOUT'] = None
        self.values['STDERR'] = None
        self.values['REQUIRES'] = []
        self.values['REQUIRES'].append('jquery')
        # Parameters
        self.parameters = OrderedDict()
        self.extra_parameters = {}
        engine_settings = self.open_settings_db()
        # Get query information
        query_fields, query_data = engine_settings.get_data(
                'SELECT description, command, parameters, shell '
                'FROM commands '
                'WHERE uuid=?',
                None,
                (self.args['UUID'], ))
        if query_data:
            self.values['DESCRIPTION'] = query_data[0][0]
            self.values['COMMAND'] = query_data[0][1].encode('utf-8').replace(
                '\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
            self.values['PARAMETERS'] = query_data[0][2].encode('utf-8')
            self.values['SHELL'] = query_data[0][3]
        else:
            self.values['ERRORS'].append('Command not found')
        if not self.values['ERRORS']:
            # Parse parameters
            if self.values['PARAMETERS']:
                list_parameters = self.values['PARAMETERS'].replace(
                    '\r\n', '\n').replace('\r', '\n').split('\n')
                for parameter in list_parameters:
                    param_name, param_config = parameter.split('=', 1)
                    # Get the parameter from the parameters table if needed
                    if param_config.startswith('parameter:'):
                        query_fields, query_data = engine_settings.get_data(
                            statement='SELECT content '
                                      'FROM parameters '
                                      'WHERE name=?',
                            replaces=None,
                            parameters=(param_config[10:], ))
                        if query_data:
                            param_config = query_data[0][0]
                            list_parameters.insert(
                                list_parameters.index(parameter),
                                '%s=%s' % (param_name, param_config))
                            list_parameters.remove(parameter)
                for parameter in list_parameters:
                    param_name, param_config = parameter.split('=', 1)
                    # Parameter configuration
                    if param_config.startswith('list:'):
                        # List of values
                        param_values = param_config[5:].split(',')
                    elif param_config.startswith('range:'):
                        # Range between two values
                        param_value1, param_value2 = param_config[6:].split('-',
                                                                            1)
                        param_values = range(
                            int(param_value1), int(param_value2) + 1)
                    elif param_config.startswith('text:'):
                        # Input text
                        param_values = ''
                    elif param_config.startswith('date:'):
                        # Date input text
                        param_values = datetime.date.today()
                        if 'jquery-ui' not in self.values['REQUIRES']:
                            self.values['REQUIRES'].append('jquery-ui')
                    elif param_config.startswith('values:'):
                        # List of key=description values
                        param_values = []
                        for param_value1 in param_config[7:].split(','):
                            param_values.append(param_value1.split('=', 1))
                    elif param_config.startswith('parameters:'):
                        param_values = []
                        for param_value1 in param_config[11:].split(','):
                            param_values.append(param_value1.split('=', 1)[0])
                    else:
                        # Not implemented parameter type
                        raise Exception('Not implemented parameter type: %s' %
                                        param_config)
                    self.parameters[param_name] = param_values
                # Check all the parameters for parameters type values
                for parameter in list_parameters:
                    param_name, param_config = parameter.split('=', 1)
                    # param_name is the parameters: name
                    if param_config.startswith('parameters:'):
                        # A parameter of type parameters has the
                        # following syntax:
                        # NAME=parameters:PARAMVALUE1=FIELD1=VALUE1, [...]
                        # [...] PARAMVALUE2=FIELD1=VALUE1
                        self.args[param_name] = self.params.get_item(param_name,
                                                                     None)
                        # self.args[param_name] is the selected PARAMVALUE
                        param_values = param_config[11:].split(',')
                        for param_values in param_values:
                            param_name2, param_values = param_values.split('=',
                                                                           1)
                            # param_name2 is each PARAMVALUE
                            # param_values is the FIELD=VALUE pairs list
                            param_values = param_values.split(';')
                            for parameter in param_values:
                                # parameter is each FIELD=value pair
                                param_value1, param_value2 = parameter.split(
                                  '=', 1)
                                # Check if the parameters parameter was set
                                if self.args[param_name] == param_name2:
                                    self.args[param_value1] = param_value2
                                else:
                                    self.args[param_value1] = None
                                self.extra_parameters[param_value1] = self.args[
                                  param_value1]
                            # Exit after the current PARAMVALUE was found
                            if self.args[param_name] == param_name2:
                                break
                        break
                # Check all the parameters if they were configured
                for parameter in self.parameters.keys():
                    self.args[parameter] = self.params.get_item(parameter, None)
                    if self.args[parameter] is not None:
                        self.args[parameter] = self.args[parameter].replace(
                            '\'', '\'\'')
                    else:
                        self.values['ERRORS'].append(
                            'Parameter %s was not provided' % parameter)
                # Fill parameters with extra parameters
                for parameter in self.extra_parameters.keys():
                    if self.extra_parameters.get(parameter, None) is not None:
                        self.args[parameter] = self.extra_parameters[
                          parameter].replace(
                            '\'', '\'\'')
        if not self.values['ERRORS']:
            self.values['STDOUT'], self.values['STDERR'] = self.process_request(
                str(self.values['COMMAND']), self.args, self.values['SHELL'])

        engine_settings.close()
        engine_settings = None
        return self.get_template(
            'run.tpl',
            ARGS=self.args,
            VALUES=self.values,
            PARAMETERS=self.parameters,
            printable_text_for_encoding=self.printable_text_for_encoding,
            date=datetime.date)

    def process_request(self, command, parameters, shell):
        """Process a command request"""
        # Convert parameters
        arguments = command % dict((str(k), str(v))
                                   for (k, v) in parameters.items())
        # For shell=True split the command in list
        if not shell:
            arguments = shlex.split(arguments)
        process = subprocess.Popen(arguments,
                                   shell=shell,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process.communicate()
