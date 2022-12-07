/*
*	회원가입
*/
var iderror = "아이디를 입력하세요.";
var passwderror = "비밀번호를 입력하세요.";
var repasswderror = "비밀번호가 다릅니다.";
var nameerror = "이름을 입력하세요.";
var emailerror = "이메일을 입력하세요";
var confirmerror = "아이디 중복확인을 해주세요";
var emailck = "이메일 형식에 맞지 않습니다"


function maincheck() {
	if(! mainform.id.value) {
		alert(iderror);
		mainform.id.focus();
		return false;
	} else if(! mainform.passwd.value) {
		alert(passwderror);
		mainform.passwd.focus();
		return false;
	}
}
//onsubmit으로 하는 방법

$(document).ready(
	function(){
		// 메인페이지
		$("form[name='mainform']").on(
			"submit",
			function(event) {
				if (! $("input[name='id']").val()){
					alert(iderror);
					$("input[name='id']").focus();
					return false;
				} else if(! $("input[name='passwd']").val()){
					alert(passwderror);
					$("input[name='passwd']").focus();
					return false;
				}
			}
		);
		
		// 회원가입
		$("form[name='inputform']").on(
			"submit",
			function(event) {
				if(! $("input[name='id']").val()) {
					alert(iderror)
					$("input[name='id']").focus();
					return false;
				} else if(! $("input[name='passwd']").val()){
					alert(passwderror)
					$("input[name='passwd']").focus();
					return false;
				} else if($ ("input[name='passwd']").val() != $("input[name='repasswd']").val()) { 
					alert(repasswderror);
					$("input[name='passwd']").focus();
					return false;
				} else if(! $("input[name='name']").val()) {
					alert(nameerror);
					$("input[name='name']").focus();
					return false;
				} else if(! $("input[name='email1']").val()) {
					alert(emailerror);
					$("input[name='email1']").focus();
					return false;
				}
				
				if($("input[name='confirm']").val()=="0") {
					alert(confirmerror);
					$("input[name='id']").focus();
					return false;
				}
				
			}
		);
		
		// 중복확인
		$("input[value='중복확인']").on(
			"click",
			function(event) {
				var id = $( "input[name='id']" ).val();
				if(! id) { 
					alert(iderror);
					$("input[name='id']").focus()
				} else {
					url = "confirm?id=" + id;
					open(url, "confirm", "toolbar=no, menubar=no, scrollbar=no, status=no, width=500, height=300");
				}
			}
		);
		
		$("td input[value='확인']").on(
			"click",
			function(event) { 
				id = $("span").text();
				$("input[name='id']", opener.document.inputform).val(id);
				$("input[name='confirm']", opener.document.inputform).val("1");
				window.close();
			}
		);	
		
		$("form[name='confirmform']").on(
			"submit",
			function(event) {
				if(! $("input[name='id']").val()) {
					alert(iderror);
					$("input[name='id']").focus();
					return false;
				}
			}
		);
		
		// 회원탈퇴
		$( "form[name='passwdform']").on(
			"submit",
			function(event) {
				if(! $("td input[name='passwd']").val()) {
					alert(passwderror)
					$("td input[name='passwd']").focus();
					return false;
				}
			}
		);
		
		// 회원정보수정
		$("form[name='modifyform']").on(
			"submit",
			function(event) {
				if(! $("input[name='passwd']").val()) {
					alert(passwderror);
					$("input[name='passwd']").focus();
					return false;
				} else if($("input[name='passwd']").val() != $("input[name='repasswd']").val()) {
					alert(repasswderror);
					$("input[name='passwd']").focus();
					return false;
				} else if(! $("input[name='email1']").val() || ! $("input[name='email2']").val()) {
					alert(emailerror);
					$("input[name='email1']").focus();
					return false;
				}
				
				if( $("input[name='email1']").val() && $("input[name='email2']").val()) {
					if($("input[name='email1']").val().indexOf("@") != -1 
					|| $("input[name='email2']").val().indexOf("@") != -1) {
						alert(emailck);
						$("input[name='email1']").focus();
						return false;
					}
				}
				
			}
		);
		
	}
);

// 아이디 중복확인
function setid(id) {
	opener.document.inputform.id.value = id
	window.close()
}


