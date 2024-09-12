$(document).ready(function() {
    // 로컬 CSV 파일에서 제품 리스트를 불러옵니다 (Python을 통해 로드된 데이터를 기반으로)
    $.getJSON("/static/data/equipment_and_products.csv", function(data) {
        var products = [];
        Papa.parse(data, {
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                results.data.forEach(function(row) {
                    if (!products.includes(row['제품'])) {
                        products.push(row['제품']);
                    }
                });

                // 제품 리스트를 화면에 동적으로 추가
                products.forEach(function(product) {
                    var productHtml = '<div class="fc-event">' + product + '</div>';
                    $('#external-events').append(productHtml);
                });

                // 각 제품을 드래그 가능하게 설정
                $('.fc-event').each(function() {
                    $(this).data('eventObject', {
                        title: $.trim($(this).text()),
                        stick: true
                    });

                    $(this).draggable({
                        zIndex: 999,
                        revert: true,
                        revertDuration: 0
                    });
                });
            }
        });
    });

    // 캘린더 초기화
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultView: 'month',
        editable: true,
        droppable: true,
        events: [],

        // 제품 클릭 시 공정/설비 정보를 가져오는 로직
        eventClick: function(event) {
            var product = event.title.split(' ')[0]; // 제품명 추출

            // CSV에서 해당 제품에 맞는 공정 및 설비 정보를 로드
            $.getJSON("/static/data/equipment_and_products.csv", function(data) {
                var processes = [];
                var equipment = [];

                Papa.parse(data, {
                    header: true,
                    skipEmptyLines: true,
                    complete: function(results) {
                        results.data.forEach(function(row) {
                            if (row['제품'] === product) {
                                processes.push(row['공정']);
                                equipment.push(row['설비1'], row['설비2']);
                            }
                        });

                        var processHtml = '<h4>공정 선택</h4><ul>';
                        processes.forEach(function(process) {
                            processHtml += '<li>' + process + '</li>';
                        });
                        processHtml += '</ul>';

                        var equipmentHtml = '<h4>설비 리스트</h4><ul>';
                        equipment.forEach(function(equip) {
                            if (equip) {
                                equipmentHtml += '<li>' + equip + '</li>';
                            }
                        });
                        equipmentHtml += '</ul>';

                        // 공정 및 설비 팝업 표시
                        $('body').append('<div id="process-popup">' + processHtml + equipmentHtml + '</div>');
                    }
                });
            });
        }
    });
});

