package com.example.demoiot;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    TextView textTemp, textHumi, textLight;
    LabeledSwitch button1, button2, button3;
    @Override

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textTemp = findViewById(R.id.txtTemp);
        textHumi = findViewById(R.id.txtHumi);
        textLight = findViewById(R.id.txtLight);
        button1 = findViewById(R.id.button1);
        button2 = findViewById(R.id.button2);
        button3 = findViewById(R.id.button3);

        button1.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if (isOn == true){
                    sendDataMQTT("HThuanN/feeds/nutnhan1","1");
                }else{
                    sendDataMQTT("HThuanN/feeds/nutnhan1","0");
                }
            }
        });
        button2.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if (isOn == true){
                    sendDataMQTT("HThuanN/feeds/nutnhan2","1");
                }else{
                    sendDataMQTT("HThuanN/feeds/nutnhan2","0");
                }
            }
        });

        button3.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if (isOn == true){
                    sendDataMQTT("HThuanN/feeds/nutnhan3","1");
                }else{
                    sendDataMQTT("HThuanN/feeds/nutnhan3","0");
                }
            }
        });

        startMQTT();
    }

    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){
        }
    }


    public void startMQTT(){
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic + "***" + message.toString());
                if(topic.contains("cambien1")){
                    textTemp.setText(message.toString() + "°C");
                }else if(topic.contains("cambien2")){
                    textHumi.setText(message.toString() + "%");
                }else if(topic.contains("cambien3")){
                    textLight.setText(message.toString() + "lx");
                }else if(topic.contains("nutnhan1")){
                    if(message.toString().equals("1")){
                        button1.setOn(true);
                    }else{
                        button1.setOn(false);
                    }
                }else if(topic.contains("nutnhan2")){
                    if(message.toString().equals("1")){
                        button2.setOn(true);
                    }else{
                        button2.setOn(false);
                    }
                }else if(topic.contains("nutnhan3")){
                    if(message.toString().equals("1")){
                        button2.setOn(true);
                    }else{
                        button2.setOn(false);
                    }
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}