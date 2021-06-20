const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const admin = require('firebase-admin');
admin.initializeApp();
const db = admin.firestore();
process.env.DEBUG = 'dialogflow:debug'; 
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function welcome(agent) {
    agent.add(`Welcome to my agent!`);
  }
 
  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
  }
  
  function Reading_control(agent) {
    const command = agent.parameters.reading_control;
    agent.add(`reading_control:${command}`);       
  }
  
  function Speed_control(agent) {
    const command = agent.parameters.change_direction;
    var number = agent.parameters.number;
    agent.add(`speed_control:${command}:${number}`);
  }

  function Volume_control(agent) {
    const command = agent.parameters.change_direction;
    var number = agent.parameters.number;
    agent.add(`volume_control:${command}:${number}`); 
  }

  function Move_control(agent) {
    const command = agent.parameters.move_direction;
    var number = agent.parameters.number;
    agent.add(`move_control:${command}:${number}`); 

}
  
  function Picture_control(agent) {
    agent.add(`picture_control`);
  }

  function Mark_make(agent) {
    const command = agent.parameters.mark_category;
    agent.add(`mark_make:${command}`);         	
  }

    function Mark_save(agent) {
    const command = agent.parameters.mark_category;
    agent.add(`mark_save:${command}`); 
  }


  function Mark_call(agent) {
    const command = agent.parameters.mark_category;
    var number = agent.parameters.number;
    agent.add(`mark_call:${command}:${number}`); 
  }
  
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('Reading_control',Reading_control);
  intentMap.set('Speed_control',Speed_control);
  intentMap.set('Volume_control',Volume_control);
  intentMap.set('Move_control',Move_control);
  intentMap.set('Picture_control',Picture_control);
  intentMap.set('Mark_make',Mark_make);
  intentMap.set('Mark_save',Mark_save);
  intentMap.set('Mark_call',Mark_call);




  agent.handleRequest(intentMap);
});