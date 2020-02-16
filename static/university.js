$(document).ready(function() {
    var userid = localStorage.getItem("userID")
    console.log(userid)

    var current_student_data = new kendo.data.DataSource({
    transport: {
        read: {
        url: "https://demos.telerik.com/kendo-ui/service/products"
        }
    }
    });

    // var current_student_data=[
    //     {
    //       "sid": "ronak@usc.edu",
    //       "sname": "Ronak Chedda",
    //       "degree": "MS in EE"
    //     },
    //     {
    //       "sid": "arpit@usc.edu",
    //       "sname": "Arpit Sharma",
    //       "degree": "MS in EE (Data Science)"
    //     },
    //     {
    //       "sid": "ruchir@usc.edu",
    //       "sname": "Ruchir Shah",
    //       "degree": "MS in CS"
    //     },
    //     {
    //       "sid": "husain@usc.edu",
    //       "sname": "Husain Zafar",
    //       "degree": "MS in CS (Game Development)"
    //     }
    // ]

    var prospective_student_data = new kendo.data.DataSource({
        transport: {
            read: {
            url: "https://demos.telerik.com/kendo-ui/service/products"
            }
        }
        });

    $("#current_students").kendoGrid({
        dataSource: current_student_data,
        selectable: true,
        columns: [{
            selectable: true,
            width: 50,
            headerTemplate: ' '
        },
        {
            field: "sid",
            title: "Student ID"
        },
        {
            field: "sname",
            title: "Student Name"
        },
        {
            field: "degree",
            title: "Degree"
        }
    ]
    })

    var currstudent_grid = $("#current_students").data("kendoGrid");
    currstudent_grid.tbody.on("click", ".k-checkbox", onClickCurrent);

    $("#prospective_students").kendoGrid({
        dataSource: prospective_student_data,
        selectable: true,
        columns: [{
            selectable: true,
            width: 50,
            headerTemplate: ' '
        },
        {
            field: "sid",
            title: "Student ID"
        },
        {
            field: "sname",
            title: "Student Name"
        },
        {
            field: "degree",
            title: "Degree"
        }]
    })

    var currstudent_grid = $("#prospective_students").data("kendoGrid");
    currstudent_grid.tbody.on("click", ".k-checkbox", onClickProspective);

    $(".current-student-btn").click(function() {
        var grid = $("#current_students").data("kendoGrid");
        var selectedItem = grid.dataItem(grid.select());
        console.log(selectedItem)
    })

    $(".prospective-student-btn").click(function() {
        var grid = $("#prospective_students").data("kendoGrid");
        var selectedItem = grid.dataItem(grid.select());
        console.log(selectedItem)
    })

    setInterval(getupdates, 2000);

})
var transaction_id=''
function getupdates() {
    console.log("get")
    $.ajax({
        url: "", 
        success: function(result){
            if (result.tid != transaction_id) {
                transaction_id = result.tid
            if (result.type == 'info') {
                $("#info").text(result);
                $("#info").show()
            }
        }
      }
    });
}

function onClickProspective(e) {
    var grid = $("#prospective_students").data("kendoGrid");
    var row = $(e.target).closest("tr");

    if(row.hasClass("k-state-selected")){
        setTimeout(function(e) {
            var grid = $("#prospective_students").data("kendoGrid");
            grid.clearSelection();
        })
    } else {
        grid.clearSelection();
    };
};

function onClickCurrent(e) {
    var grid = $("#current_students").data("kendoGrid");
    var row = $(e.target).closest("tr");

    if(row.hasClass("k-state-selected")){
        setTimeout(function(e) {
            var grid = $("#current_students").data("kendoGrid");
            grid.clearSelection();
        })
    } else {
        grid.clearSelection();
    };
};
