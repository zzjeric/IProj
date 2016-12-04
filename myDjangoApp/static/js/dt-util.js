/**
 * 获取本周,上周,下周开始日期、结束日期
 */
var now = new Date(); //当前日期
var nowDayOfWeek = now.getDay(); //今天本周的第几天
var nowDay = now.getDate(); //当前日
var nowMonth = now.getMonth(); //当前月
var nowYear = now.getYear(); //当前年
nowYear += (nowYear < 2000) ? 1900 : 0; //
//格式化日期：yyyy/MM/dd
function formatDate(date) {
    var myyear = date.getFullYear();
    var mymonth = date.getMonth() + 1;
    var myweekday = date.getDate();
    if (mymonth < 10) {
        mymonth = "0" + mymonth;
    }
    if (myweekday < 10) {
        myweekday = "0" + myweekday;
    }
    return (myyear + "/" + mymonth + "/" + myweekday);
}

//获得本周的开始日期
function getWeekStartDate() {
	var myYear = nowYear;
	var myDay = nowDay - nowDayOfWeek + 1;
    if(nowMonth == 0 && myDay < 0){
    	myYear = nowYear - 1;
    }
    var weekStartDate = new Date(myYear, nowMonth, myDay );
    return formatDate(weekStartDate);
}
//获得本周的结束日期
function getWeekEndDate() {
	var myYear = nowYear;
	var myDay = nowDay + (6 - nowDayOfWeek) + 1;
    // if(nowMonth == 11 && myDay > 31){
    // 	myYear = nowYear + 1;
    // }
    var weekEndDate = new Date(nowYear, nowMonth, myDay);
    return formatDate(weekEndDate);
}
//获得上周的开始日期
function getLastWeekStartDate() {
	var myYear = nowYear;
	var myDay = nowDay - nowDayOfWeek - 7 + 1;
    // if(nowMonth == 0 && myDay < 0){
    // 	myYear = nowYear - 1;
    // }
    var weekStartDate = new Date(nowYear, nowMonth, nowDay - nowDayOfWeek - 7 + 1);
    return formatDate(weekStartDate);
}
//获得上周的结束日期
function getLastWeekEndDate() {
	var myYear = nowYear;
	var myDay = nowDay - nowDayOfWeek - 1 + 1;
    // if(nowMonth == 0 && myDay < 0){
    // 	myYear = nowYear - 1;
    // }
    var weekEndDate = new Date(nowYear, nowMonth, myDay);
    return formatDate(weekEndDate);
}
//获得下周的开始日期
function getNextWeekStartDate() {
    var myYear = nowYear;
	var myDay = nowDay - nowDayOfWeek + 7 + 1;
    // if(nowMonth == 11 && myDay > 31){
    // 	myYear = nowYear + 1;
    // }
    var weekStartDate = new Date(nowYear, nowMonth, myDay);
    return formatDate(weekStartDate);
}
//获得下周的结束日期
function getNextWeekEndDate() {
    var myYear = nowYear;
	var myDay = nowDay - nowDayOfWeek + 14 + 1;
    // if(nowMonth == 11 && myDay > 31){
    // 	myYear = nowYear + 1;
    // }
    var weekEndDate = new Date(nowYear, nowMonth, myDay);
    return formatDate(weekEndDate);
}
