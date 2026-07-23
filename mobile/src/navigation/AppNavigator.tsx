import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { ActivityIndicator, View } from "react-native";
import { useAuth } from "../contexts/AuthContext";
import LoginScreen from "../screens/LoginScreen";
import CadastroScreen from "../screens/CadastroScreen";
import NovaOcorrenciaScreen from "../screens/NovaOcorrenciaScreen";
import HistoricoScreen from "../screens/HistoricoScreen";

const Stack = createNativeStackNavigator();

export function AppNavigator() {
  const { usuario, carregando } = useAuth();

  if (carregando) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <ActivityIndicator size="large" color="#0B6E4F" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerTitleAlign: "center" }}>
        {usuario ? (
          <>
            <Stack.Screen
              name="NovaOcorrencia"
              component={NovaOcorrenciaScreen}
              options={{ title: "Nova Ocorrência" }}
            />
            <Stack.Screen
              name="Historico"
              component={HistoricoScreen}
              options={{ title: "Minhas Ocorrências" }}
            />
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen name="Cadastro" component={CadastroScreen} options={{ title: "Criar conta" }} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
