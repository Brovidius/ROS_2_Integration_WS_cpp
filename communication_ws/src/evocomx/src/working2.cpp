#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string.h>
#include <chrono>
#include <unistd.h>
#include <signal.h>
#include <string>
#include <vector>
#include <sstream>
#include <ctime>
#include <cstdio>
#include <stdio.h>
#include <functional>
#include <memory>

// #include "nodecomx_cpp_py/cpp_header.hpp"
#include "lib/Evo_janusXsdm/Evo_janusXsdm.cpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"


//Constructor parameters for Evo_janusXsdm.h
std::string JANUS_PATH = "src/evocomx/include/lib/janus-c-3.0.5/bin/";
std::string SDM_PATH = "src/evocomx/include/lib/sdmsh/";
std::string IP ="192.168.0.198";
int JANUS_RX_PORT = 9921;
int JANUS_TX_PORT = 9915;
float STREAMFS = 250000.0;

// RX varaibles
int timeout = 500; // milliseconds [ms] should be low
std::string response;
std::string comment;
int fd_listen;


Evo_janusXsdm::connection modem(IP, JANUS_PATH, SDM_PATH, JANUS_RX_PORT, JANUS_TX_PORT, STREAMFS);

class ComPubNode : public rclcpp::Node
{
public:
    ComPubNode() : Node("Evo")
    {
        // Configures modem and sets preamble
        modem.sdmConfigAir();
        std::this_thread::sleep_for(500ms);
        modem.setPreamble();
        std::this_thread::sleep_for(500ms);

        // Create subscriber
        subscriber_ = this->create_subscription<std_msgs::msg::String>
        (
            "/topic_transmission", 
            10, 
            std::bind(&ComPubNode::callback, this, std::placeholders::_1)
        );

        // Create publisher
        publisher_ = this->create_publisher<std_msgs::msg::String>
        (
            "/topic_reception", 
            10
        );
        // timer_ = this->create_wall_timer
        // (
        //     100ms, 
        //     std::bind(&ComPubNode::timer_callback, this)
        // );
        RCLCPP_INFO(this->get_logger(), "Node has been started.");
        loop();
    }

private:
    // rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
    std::string modemMSG;
    bool update = 0;
    bool listen = 1;

    void callback (const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "From Topic: '%s'", msg->data.c_str());
        modemMSG = msg->data;
        update = 1;

    }

    void loop ()
    {
       // Listen to modem
        fd_listen = modem.startRX();

        while (rclcpp::ok())
        {
            modem.listenRX(fd_listen, response, timeout);
            if (response != "NaN") 
            {
                // Populate and publish message
                auto message = std_msgs::msg::String();
                message.data = response;
                // message.data = "response";
                RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
                publisher_->publish(message);
            }
            std::cout << "bool: " << update << std::endl;
            if (update == 1) 
            {
                modem.closePipeRX(fd_listen);
                std::this_thread::sleep_for(500ms);
                modem.startTX(modemMSG);
                std::this_thread::sleep_for(1000ms);
                update = 0;
                fd_listen = modem.startRX();

            } 
            rclcpp::spin_some(this->get_node_base_interface());
        }
        std::cout << "ROS closing pipe\n";
        modem.closePipeRX(fd_listen);
        modem.stopRX();
    }

    // void timer_callback()
    // {
    //     // Listen to modem
    //     if (listen == 1)
    //     {
    //         fd_listen = modem.startRX();
    //         listen = 0;
    //     }
    //     // std::array<std::string,4> responsFromFrame = modem.listenOnceRXsimple(response,timeout);
    //     // std::cout << "listen to modem\n";

    //     modem.listenRX(fd_listen, response, timeout);

    //     if (response != "NaN") 
    //     {
    //         // Populate and publish message
    //         auto message = std_msgs::msg::String();
    //         message.data = response;
    //         // message.data = "response";
    //         RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    //         publisher_->publish(message);
    //     }
    //     // std::cout << "bool: " << update << "\n";
    //     if (update == 1) 
    //     {
    //         modem.closePipeRX(fd_listen);
    //         std::this_thread::sleep_for(500ms);
    //         modem.startTX(modemMSG);
    //         // std::cout << "Sent data to modem: " << modemMSG <<"\n";
    //         update = 0;
    //         listen = 1;
    //     }
    // }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ComPubNode>());
    std::cout << "ROS closing pipe\n";
    modem.closePipeRX(fd_listen);
    modem.stopRX();
    rclcpp::shutdown();
    return 0;
}
