// Dynamic size selection based on size type in Django Admin

(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Get the size_type and available_sizes fields
        const sizeTypeSelect = $('#id_size_type');
        const availableSizesField = $('#id_available_sizes');
        const availableSizesFieldset = availableSizesField.closest('.form-row');
        
        // Store the original checkbox creation function
        const originalCheckboxSelectInputs = availableSizesField.data('checkbox-select-inputs');
        
        // Size options for each type
        const sizeOptions = {
            'jeans': ['28', '30', '32', '34', '36', '38', '40'],
            'shirt': ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'],
            'shoes': ['37', '38', '39', '40', '41', '42', '43'],
            'one_size': ['OS'],
            'none': []
        };
        
        // Update available sizes field based on size type
        function updateAvailableSizes() {
            const selectedType = sizeTypeSelect.val();
            const options = sizeOptions[selectedType] || [];
            
            // Clear existing options
            availableSizesField.empty();
            
            // Add new options
            if (options.length > 0) {
                options.forEach(function(size) {
                    availableSizesField.append(
                        $('<option></option>').val(size).text(size)
                    );
                });
                
                // Show the field
                availableSizesFieldset.show();
            } else {
                // Hide the field if no sizes
                availableSizesFieldset.hide();
            }
        }
        
        // Initialize on page load
        updateAvailableSizes();
        
        // Update when size type changes
        sizeTypeSelect.change(function() {
            updateAvailableSizes();
        });
    });
})(django.jQuery);

