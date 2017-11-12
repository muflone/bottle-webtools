<!DOCTYPE html>
<html>
    <head>
        <title>{{ VALUES['DESCRIPTION'] }}</title>
        <link type="text/css" rel="stylesheet" href="static/css/styles.css">
        <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
        <link type="text/css" rel="stylesheet" href="static/css/table.css">
        <link type="text/css" rel="stylesheet" href="static/css/run.css">
        <link type="text/css" rel="stylesheet" href="static/jquery/jquery-ui-1.11.4.min.css">
        <link type="text/css" rel="stylesheet" href="static/jquery/jquery-ui.theme-1.11.4.min.css">
        <script type="text/javascript" src="static/jquery/jquery-1.11.3.min.js"></script>
        <script type="text/javascript" src="static/jquery/jquery-ui-1.11.4.min.js"></script>
    </head>

    <body>
% include('%s/includes/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
% if PARAMETERS:
        <form method="get">
            <input type="hidden" name="uuid" value="{{ ARGS['UUID'] }}">
            <table id="parameters">
                <caption>Query parameters</caption>
                <tbody>
    % for PARAM_NAME in PARAMETERS.keys():
      % print PARAM_NAME, type(PARAMETERS[PARAM_NAME]), type(ARGS[PARAM_NAME]), ARGS[PARAM_NAME]
                    <tr>
                        <th>{{PARAM_NAME }}</th>
        % if type(PARAMETERS[PARAM_NAME]) is list:
                        <td><select name="{{ PARAM_NAME }}">
            % if type(PARAMETERS[PARAM_NAME][0]) is list:
                % include('%s/includes/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS[PARAM_NAME], DATA=PARAMETERS[PARAM_NAME])
            % else:
                % include('%s/includes/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS[PARAM_NAME], DATA=[(value, value) for value in PARAMETERS[PARAM_NAME]])
            % end
                        </select></td>
        % elif type(PARAMETERS[PARAM_NAME]) is str:
                        <td><input type="text" name="{{ PARAM_NAME }}" value="{{ ARGS[PARAM_NAME] if ARGS[PARAM_NAME] is not None else '' }}"></td>
        % elif type(PARAMETERS[PARAM_NAME]) is date:
                        <td><input type="text" name="{{ PARAM_NAME }}" value="{{ ARGS[PARAM_NAME] if ARGS[PARAM_NAME] is not None else '' }}" id="{{ PARAM_NAME.replace(' ', '_') }}"></td>
                        <script>
                            $( "#{{ PARAM_NAME.replace(' ', '_') }}" ).datepicker({
                                dateFormat: "yy-mm-dd",
                            });
                        </script>
        % end
                    </tr>
    % end
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="2">
                            <input type="submit" name="confirm" value="Confirm">
                        </td>
                    </tr>
                </tfoot>
            </table>
        </form>
% end
% if VALUES['STDOUT'] or VALUES['STDERR']:
        <!-- Begin of response data -->
        <table id="command_result">
            <caption>Command result</caption>
            <tbody>
                <tr>
                    <th>Command output</th>
                    <td><textarea name="stdout" readonly>{{ VALUES['STDOUT'] }}</textarea></td>
                </tr>
                <tr>
                    <th>Command error</th>
                    <td><textarea name="stderr" readonly>{{ VALUES['STDERR'] }}</textarea></td>
                </tr>
            </tbody>
        </table>
        <!-- End of response data -->
% end
    </body>
</html>
