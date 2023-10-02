$(window).ready(function(){
  var table= $('#myTable').DataTable( {
    columnDefs: [ {
            orderable: false,
            className: 'select-checkbox',
            targets:   0
        } ],
        select: {
            style:    'os',
            selector: 'td:first-child'
        },
        order: [[ 1, 'asc' ]],
    responsive: {
        details: {
            display: $.fn.dataTable.Responsive.display.childRow,
            type: ''
        }
    }
  });

  $('#dismiss, .overlay').on('click', function () {
    $('#sidebar').removeClass('active');
    $('.overlay').removeClass('active');
  });

  $('#sidebarCollapse').on('click', function () {
    $('#sidebar').addClass('active');
    $('.overlay').addClass('active');
    $('a[aria-expanded=true]').attr('aria-expanded', 'false');
  });

});
