import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';
import { supabase } from './supabase';

export const notificationService = {
  async registerForPushNotificationsAsync() {
    let token;
    if (Platform.OS === 'web') {
      throw new Error('Push notifications not supported on web');
    }

    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    if (finalStatus !== 'granted') {
      alert('Failed to get push token for push notifications!');
      return;
    }

    token = (await Notifications.getExpoPushTokenAsync()).data;
    
    // Guardar el token en la tabla profiles de Supabase
    const { user } = await supabase.auth.getUser();
    if (user) {
      await supabase
        .from('profiles')
        .update({ push_token: token })
        .eq('id', user.id);
    }
    
    return token;
  },

  // Configurar cómo se comportan las notificaciones cuando la app está abierta
  setNotificationHandler() {
    Notifications.setNotificationHandler({
      handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: false,
      }),
    });
  }
};
