AOS.init();

// 가사로 불러오기
window.onload = () => {
    $('.input_text').focus(function() {
        $('.input_text').removeAttr('placeholder')
    });
    $('.input_text').blur(function() {
        $('.input_text').attr('placeholder','제목 또는 가사를 입력하세요')
    });

    // 제목 검색 버튼 눌렸을 시 동작
    $('.title_btn').click(function() {
        if($('.result')) {
            $('body').append($('footer'))
            $('.result').remove()
        }
        getSongByTitle()
    });

    // 가사 관련 시대 검색 버튼 눌렸을 시 동작
    $('.lyrics_btn').click(function() {
        if($('.result')) {
            $('body').append($('footer'))
            $('.result').remove()
        }
        getSongByLyrics()
    });
}

// 서버호출
const callServer = async action => {
    const input = $('.input_text').val()
    res = await fetch(`/${action}?data=${encodeURIComponent(input)}`)
    return res.json() // key : columns, index, data  
}

// 반환받은 json 데이터 활용하기 좋게 변환
const converting = json => {
    song_info = new Object()
    for (i = 0; i < json['index'].length; i++){
        song_info[i] = new Object()
        for (j in json['columns']) 
            song_info[i][json['columns'][j]] = json['data'][i][j]
    }
    
    return song_info
}

function focus_result() {
    var scrollPosition = $("#result").offset().top;

    $('html, body').animate({
        scrollTop: scrollPosition-100
    }, 500);
}

// 가사입력시 유사한 음악 30개
async function getSongByLyrics() {
    if($('.input_text').val() == "")
        alert("제목이나 가사를 입력하세요")
    else {
        data = await callServer('lyrics')

        song_info = converting(data['data']) // 가사값에 대한 필요 데이터 30개

        $(".container").after(
            `<div class="result" id="result">
                <div class="result_since">
                    ${data['since'][0]}년도와 ${data['since'][1]}년도 노래를 추천드립니다
                </div>
                <div class="result_music">
                </div>
            </div>`
        );

        i = 0
        while(song_info[i] != null) {
            $(".result_music").append( 
                `<div class='music' data-aos='fade-up-left' data-aos-delay=${i*50}>
                    <img src=${song_info[i]['img']} class='image'>
                    <div class='info'>
                        <div class='name'>
                            <a href="https://www.melon.com/song/detail.htm?songId=${song_info[i]['id']}" target="_blank">${song_info[i]['name']}</a>
                        </div>
                        <div class='singer'>
                            <a href="https://www.melon.com/search/total/index.htm?q=${encodeURI(song_info[i]['singer'])}&section=&linkOrText=T&ipath=srch_form" target="_blank">${song_info[i]['singer']}</a>  
                        </div>
                        <div class='genre'>${song_info[i]['jenre']}</div>
                    </div>
                </div>`
            );
            i++;
        }

        $('.result_music').append($('footer'))
        focus_result()
    }
}

// 제목 입력시 유사한 음악 30개
async function getSongByTitle() {
    if($('.input_text').val() == "")
        alert("제목이나 가사를 입력하세요")
    else {
        data = await callServer('title')

        song_info = converting(data) // 가사값에 대한 필요 데이터 30개

        $(".container").after(
            `<div class="result" id="result">
                <div class="result_music">
                </div>
            </div>`
        );

        i = 0
        while(song_info[i] != null) {
            $(".result_music").append( 
                `<div class='music' data-aos='fade-up-left' data-aos-delay=${i*50}>
                    <img src=${song_info[i]['img']} class='image'>
                    <div class='info'>
                        <div class='name'>
                            <a href="https://www.melon.com/song/detail.htm?songId=${song_info[i]['id']}" target="_blank">${song_info[i]['name']}</a>
                        </div>
                        <div class='singer'>
                            <a href="https://www.melon.com/search/total/index.htm?q=${encodeURI(song_info[i]['singer'])}&section=&linkOrText=T&ipath=srch_form" target="_blank">${song_info[i]['singer']}</a>  
                        </div>
                        <div class='genre'>${song_info[i]['jenre']}</div>
                    </div>
                </div>`
            );
            i++;
        }

        $('.result_music').append($('footer'))
        focus_result()
    }
}
