document.addEventListener('DOMContentLoaded', function () {
    var datalist = document.getElementById('facilities');

    var facilities = {{ data['facilities']|tojson }};

    document.getElementById("nests").addEventListener("change", function () {
        var selectedValue = this.value;

        if (selectedValue === 'select') {
            document.getElementById("nests").style.borderColor = 'red';
            alert('Please Select A Valid Nest');
        }
        else {
            document.getElementById("nests").style.borderColor = 'blue';

            var selectedFacilities = facilities[selectedValue];

            selectedFacilities.forEach(function(facility) {
                var option = document.createElement('option');
                option.value = facility;
                datalist.appendChild(option);
            });

        }
    });
});




// var xhr = new XMLHttpRequest();
//         xhr.open("POST", "/fetch");
//         xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//         xhr.addEventListener('load', function (event) {
//             if (xhr.status >= 200 && xhr.status < 300) {
//                 // location.reload();
//             }
//         });
//         xhr.send(JSON.stringify({
//             "nest": selectedValue
//         }));