import React, { useState } from "react";
import { GiftedChat } from "react-native-gifted-chat";
import Icon from "react-native-vector-icons/MaterialIcons";
import image from "./assets/chat_back.jpeg";

import {
  View,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Text,
  ImageBackground,
} from "react-native";

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");

  const handleSend = () => {
    console.log(inputText);
    if (inputText.trim() === "") {
      return;
    }

    const newMessage = {
      _id: messages.length + 1,
      text: inputText,
      createdAt: new Date(),
      user: { _id: 1, name: "User" },
    };

    setMessages((prevMessages) =>
      GiftedChat.append(prevMessages, [newMessage])
    );
    setInputText("");

    // Replace the API_ENDPOINT with your server API endpoint
    fetch("http://10.5.212.110:5000/process_input", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_input: inputText }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const botResponse = {
          _id: messages.length + 2,
          text: data.filtered_response,
          createdAt: new Date(),
          user: { _id: 2, name: "medical Bot" },
        };
        setMessages((prevMessages) =>
          GiftedChat.append(prevMessages, [botResponse])
        );
      })
      .catch((error) => {
        console.error("error", error);
      });
  };

  return (
    <View style={styles.container}>
      <ImageBackground source={image} style={styles.image}>
        <GiftedChat
          messages={messages}
          onSend={handleSend}
          user={{ _id: 1, name: "User" }}
          renderInputToolbar={() => (
            <View style={styles.inputToolbar}>
              <TextInput
                style={styles.textInput}
                placeholder="Type how you feel..."
                value={inputText}
                onChangeText={(text) => setInputText(text)}
              />
              <TouchableOpacity onPress={handleSend} style={styles.sendButton}>
                <Icon
                  name="send"
                  size={30}
                  color="white"
                  style={styles.searchIcon}
                />
              </TouchableOpacity>
            </View>
          )}
        />
      </ImageBackground>
    </View>

    // const ChatScreen = () => {
    //   const [messages, setMessages] = useState([]);
    //   const [inputText, setInputText] = useState("");

    //   const handleSend = () => {
    //     if (inputText.trim() === "") {
    //       return;
    //     }

    //     const newMessage = {
    //       _id: messages.length + 1,
    //       text: inputText,
    //       createdAt: new Date(),
    //       user: { _id: 1, name: "User" },
    //     };

    //     setMessages((prevMessages) =>
    //       GiftedChat.append(prevMessages, [newMessage])
    //     );
    //     setInputText("");

    //     // Simulate bot response after a delay
    //     setTimeout(() => {
    //       const botResponse = {
    //         _id: messages.length + 2,
    //         text: "Hello! I am a medical Bot.",
    //         createdAt: new Date(),
    //         user: { _id: 2, name: "medical Bot" },
    //       };
    //       setMessages((prevMessages) =>
    //         GiftedChat.append(prevMessages, [botResponse])
    //       );
    //     }, 1000);
    //   };

    //   return (
    //     <View style={styles.container}>
    //       <ImageBackground source={image} style={styles.image} blurRadius={3}>
    //         <GiftedChat
    //           messages={messages}
    //           onSend={handleSend}
    //           user={{ _id: 1, name: "User" }}
    //           renderInputToolbar={() => (
    //             <View style={styles.inputToolbar}>
    //               <TextInput
    //                 style={styles.textInput}
    //                 placeholder="Type how you feel..."
    //                 value={inputText}
    //                 onChangeText={(text) => setInputText(text)}
    //               />
    //               <TouchableOpacity onPress={handleSend} style={styles.sendButton}>
    //                 <Icon
    //                   name="send"
    //                   size={30}
    //                   color="white"
    //                   style={styles.searchIcon}
    //                 />
    //               </TouchableOpacity>
    //             </View>
    //           )}
    //         />
    //       </ImageBackground>
    //     </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginBottom: 40,

    // Adjust the margin as needed
  },
  image: {
    flex: 1,
    resizeMode: "cover",
    justifyContent: "center",
  },
  inputToolbar: {
    flexDirection: "row",
    alignItems: "center",
    padding: 10,
    // backgroundColor: "red",

    // opacity: 100,
  },
  textInput: {
    flex: 1,
    height: 60,
    borderColor: "gray",
    borderWidth: 2,
    borderStyle: "dotted",
    borderRadius: 20,
    paddingLeft: 10,
    backgroundColor: "white",
  },
  sendButton: {
    marginLeft: 10,
  },
  searchIcon: {
    backgroundColor: "blue",
    height: 50,
    width: 60,
    textAlign: "center",
    verticalAlign: "middle",
    borderRadius: 15,
  },
});

export default ChatScreen;
