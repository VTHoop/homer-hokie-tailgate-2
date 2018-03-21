 $().ready(function(){
     // alias required to cRequired with new message
     $.validator.addMethod("dDigits", $.validator.methods.digits, "Numbers only");
     $.validator.addClassRules("dashboard-input", { dDigits: true });
     
     $("#dashboardScores").validate();
     
     });