function allNumbers(e){
   var key;
   if(window.event){
      key = e.keyCode;
   }else if(e.which){
      key = e.which;
   }
    
    if (key == 8 || key == 13){//backspace
	return true;
    }else if(key==9){//tab
	return true;
    }else if(key==37 || key==39){//37 <-, 39 ->
	return true;
    }else if(key >= 96 && key <=105){//numpad 0-9 numbers
	return true;
    }else if (key < 48 || key > 57){//alpha characters
	return false;
    }else{
	return true;
    }

}


function Decimals(e){
  var key;
   if(window.event){
      key = e.keyCode;
   }else if(e.which){
      key = e.which;
   }

  if (key == 8 || key == 13){//backspace
    return true;
  }else if(key==9){//tab
    return true;
  }else if(key==37 || key==39){//37 <-, 39 ->
    return true;
  }else if(key==110){//numpad period
    return true;
  }else if(key==190){//decimal point
    return true;
  }else if(key >= 96 && key <=105){//numpad 0-9 numbers
    return true;
  }else if (key < 48 || key > 57){//alpha characters
    return false;
  }else{
    return true;
  }
}

function emptyStr(str) {
  var i = 0;
  var length = str.length;
                     
  for (i = 0; i < length; i++) {
     if (str.charAt(i) != ' ')
        return false;
  }               
        return true;    
}

//this function will validate a string if it is 
//a valid date format mm/dd/yyyy


