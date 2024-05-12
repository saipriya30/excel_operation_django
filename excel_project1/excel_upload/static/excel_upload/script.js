// script.js

$(document).ready(function() {
    // Save All Changes
    $('#saveChangesBtn').click(function() {
        var updatedRows = {};

        $('#excelTable tbody tr').each(function() {
            var rowId = $(this).data('row-id').toString();  // Convert row ID to string
            var rowData = {};

            $(this).find('input').each(function() {
                var columnName = $(this).attr('name');
                var value = $(this).val();
                rowData[columnName] = value;
            });

            updatedRows[rowId] = rowData;
        });

        var data = {
            'excel_file_id': '{{ excel_file.id }}',  // Assuming you're passing the Excel file ID to the template
            'updated_rows': updatedRows
        };

        $.ajax({
            type: 'POST',
            url: '{% url "save_all_changes" %}',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    window.location.href = '{% url "display_table" %}';  // Redirect to display_table view
                } else {
                    console.error('Error saving all changes:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', error);
            }
        });
    });
});
