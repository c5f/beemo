
var Call = function(object) {

    this.number = object["number"];
    this.participant = object["participant"];
    this.completed_date = object["completed_date"];
    this.goal_met = object["goal_met"];
    this.veg_servings = object["veg_servings"];
    this.fruit_servings = object["fruit_servings"];
    this.fiber_grams = object["fiber_grams"];
    this.fat_grams = object["fat_grams"];
    this.steps = object["steps"];
    this.adherence_score = object["adherence_score"];

}

var Participant = function(object) {

    this.pid = object["pid"]
    this.creation_date = object["creation_date"]
    this.sms_number = object["sms_number"]
    this.base_fat_goal = object["base_fat_goal"]
    this.base_step_goal = object["base_step_goal"]
    this.emails_in = object["emails_in"]
    this.emails_out = object["emails_out"]
    this.calls_in = object["calls_in"]
    this.calls_out = object["calls_out"]
    this.sms_in = object["sms_in"]
    this.sms_out = object["sms_out"]
    this.phone_numbers = object["phone_numbers"]

}
