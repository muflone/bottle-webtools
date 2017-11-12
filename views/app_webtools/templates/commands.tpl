<!DOCTYPE html>
<html>
    <head>
        <title>Configure commands</title>
        <link type="text/css" rel="stylesheet" href="static/css/styles.css">
        <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
        <link type="text/css" rel="stylesheet" href="static/css/table.css">
        <link type="text/css" rel="stylesheet" href="static/jquery/jquery-ui-1.11.4.min.css">
        <link type="text/css" rel="stylesheet" href="static/jquery/jquery-ui.theme-1.11.4.min.css">
        <link type="text/css" rel="stylesheet" href="static/fancytree-2.11.0/skin-lion/ui.fancytree.min.css">
        <script type="text/javascript" src="static/jquery/jquery-1.11.3.min.js"></script>
        <script type="text/javascript" src="static/jquery/jquery-ui-1.11.4.min.js"></script>
        <script type="text/javascript" src="static/fancytree-2.11.0/jquery.fancytree-all.min.js"></script>
        <script type="text/javascript" src="static/fancytree-2.11.0/jquery.fancytree.table.js"></script>
        <!-- Initialize the tree when the page is loaded -->
        <script type="text/javascript">
            $(function(){
                // Create the tree inside the <table id="treetable"> element
                $("#treetable").fancytree({
                    extensions: ["table"],
                    table: {
                        indentation: 0,         // indent 0px per node level
                        nodeColumnIdx: 1,       // render the node title into the 2nd column
                        checkboxColumnIdx: 1    // render the checkboxes into the 1st column
                    }, // End of table field
                    source: {
                        url: "?format=json"
                    }, // End of source field
                    checkbox: false,
                    clickFolderMode: 4, // 1:activate, 2:expand, 3:activate and expand, 4:activate (dblclick expands)
                    renderColumns: function(event, data) {
                        var node = data.node;
                        var $tdList = $(node.tr).find(">td");
                        if (!node.isFolder()) {
                            $tdList.eq(0).html('<a href="run?uuid=' + node.key + '"><img src="static/images/run.png"></a>');
                        }
                        $tdList.eq(2).text(node.tooltip);
                    } // End of renderColumns field
                }); // End of fancytree definition
            }); // End of document function
        </script>
    </head>

    <body>
% include('%s/includes/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
        <!-- Begin of request form -->
        <form method="get" accept-charset="UTF-8">
            <input type="hidden" name="uuid" value="{{ ARGS['UUID'] }}">
            <table id="parameters">
                <caption>Command configuration</caption>
                <tbody>
                    <tr>
                        <th>Folder:</th>
                        <td><select name="folder">
% include('%s/includes/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS['FOLDER'], DATA=VALUES['FOLDERS'])
                        </select></td>
                    </tr>
                    <tr>
                        <th>Command name:</th>
                        <td><input type="text" name="name" value="{{ ARGS['NAME'] }}"></td>
                    </tr>
                    <tr>
                        <th>Description:</th>
                        <td><input type="text" name="description" value="{{ ARGS['DESCRIPTION'] }}"></td>
                    </tr>
                    <tr>
                        <th>Command:</th>
                        <td><textarea name="command" id="codemirror" placeholder="< COMMAND TEXT >">{{ ARGS['COMMAND'] }}</textarea></td>
                    </tr>
                    <tr>
                        <th>Parameters:</th>
                        <td><textarea name="parameters">{{ ARGS['PARAMETERS'] }}</textarea></td>
                    </tr>
                    <tr>
                        <th>Shell:</th>
                        <td>\\
% include('%s/includes/input_check.inc' % MODULE, NAME='shell', VALUE='1', SELECTED=ARGS['SHELL'], TITLE='Command uses shell')
</td>
                    </tr>
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="2">
                            <input type="submit" name="confirm" value="Confirm">
% if ARGS['NAME'] and not VALUES['ERRORS']:
                            <input type="button" name="cancel" value="Cancel" onclick="javascript:location.href='commands';">
                            <input type="submit" name="delete" value="Delete">
% end
                        </td>
                    </tr>
                </tfoot>
            </table>
        </form>
        <!-- End of request form -->

% if VALUES['DATA']:
        <hr />
        <!-- Begin of response data -->
        <table id="treetable" class="data">
            <colgroup>
                <col width="36px"></col>
                <col></col>
                <col></col>
            </colgroup>
            <caption>Existing commands</caption>
            <thead>
                <tr>
                    <th>Run</th>
                    <th>Name</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
% end
        <!-- End of response data -->
% include('%s/includes/footer.inc' % MODULE)
    </body>
</html>
