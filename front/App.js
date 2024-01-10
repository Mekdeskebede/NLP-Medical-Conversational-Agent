import React, { useState } from "react";
import { GiftedChat } from "react-native-gifted-chat";
import Icon from "react-native-vector-icons/MaterialIcons";

import {
  View,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Text,
} from "react-native";

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");

  const handleSend = () => {
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

    // Simulate bot response after a delay
    setTimeout(() => {
      const botResponse = {
        _id: messages.length + 2,
        text: "Hello! I am a medical Bot.",
        createdAt: new Date(),
        user: { _id: 2, name: "medical Bot" },
      };
      setMessages((prevMessages) =>
        GiftedChat.append(prevMessages, [botResponse])
      );
    }, 1000);
  };

  return (
    <View style={styles.container}>
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
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginBottom: 40, // Adjust the margin as needed
  },
  inputToolbar: {
    flexDirection: "row",
    alignItems: "center",
    padding: 10,
    // backgroundColor: "white",
    // opacity: 100,
  },
  textInput: {
    flex: 1,
    height: 60,
    // borderColor: "gray",
    // borderWidth: 1,
    borderRadius: 20,
    paddingLeft: 10,
    backgroundColor: "white",
  },
  sendButton: {
    marginLeft: 10,
  },
  searchIcon: {
    backgroundColor: "#C276F0",
    height: 50,
    width: 60,
    textAlign: "center",
    verticalAlign: "middle",
    borderRadius: 15,
  },
});

export default ChatScreen;