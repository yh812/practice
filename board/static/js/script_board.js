/**
 * 게시판
 */
 
var writererror = "작성자를 입력하세요"
var subjecterror = "글제목을 입력하세요"
var contenterror = "글내용을 입력하세요"
var passwderror = "비밀번호를 입력하세요"
 
 $(document).ready(
	function(){
		
		// 글쓰기
		$("form[name='inputform']").on(
			"submit",
			function(event) {
				if(! $("input[name='writer']").val()){
					alert(writererror);
					$("input[name='writer']").focus();
					return false;
				} else if(! $("input[name='subject']").val()) {
					alert(subjecterror);
					$("input[name='subject']").focus();
					return false;
				} else if(! $("textarea[name='content']").val()) {
					alert(contenterror);
					$("input[name='content']").focus();
					return false;
				} else if(! $("input[name='passwd']").val()) {
					alert(passwderror);
					$("input[name='passwd']").focus();
					return false;
				}
			}
		);
		
		// 비밀번호 확인
		$("form[name='passwdform']").on(
			"submit",
			function(event) {
				if(! $("input[name='passwd']").val()) {
					alert(passwderror);
					$("input[name='passwd']").focus();
					return false;
				}
			}
		);
	}
);