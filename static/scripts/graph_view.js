function plotGraph(nodes, edges) {
    var G = new jsnx.Graph();

    G.addNodesFrom(nodes, {color: '#0064C7'});
    G.addEdgesFrom(edges);

    jsnx.draw(G, {
        element: '#centered',
        withLabels: true,
        layoutAttr: {
            charge: -500
        },
        nodeStyle: {
            fill: function(d) {
                return d.data.color;
            }
        },
        labelStyle: {fill: 'white'},
        stickyDrag: true
    });
    d3.selectAll('#centered svg').style('opacity', 0.01).transition().duration(1500).style('opacity', 1);
}

function changePlot(current_id) {
    $.post('/change_graph', {
        send_id: current_id
    }).done(function(changes) {
        $('.active').removeClass('active');
        $("#graph"+current_id).attr('class', "list-group-item active");
        plotGraph(changes['nodes'],changes['edges']);
    });
}

function uploadExcelFile() {
    var $input = $("#uploadfile");
    var fd = new FormData;

    fd.append('file', $input.prop('files')[0]);

    $.ajax({
        url: '/upload_file',
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(changes) {
            var text = "";
            text += changes["name"] + '   ' + changes["load_date"];
            $('.active').removeClass('active');
            $("#list_of_files").prepend(
                    $('<a>').attr({'href': "javascript:changePlot('" + changes['id'] + "');",
                                  'class': "list-group-item active",
                                  'id': "graph" + changes['id']
                                  }).append(text));
            $('#list_of_files').animate({
                                 scrollTop: $("#graph" + changes['id']).position().top
                                 }, 'slow');
            plotGraph(changes['content']['nodes'],changes['content']['edges']);
        }
    });
}