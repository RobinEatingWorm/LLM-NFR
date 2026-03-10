package ch.hearc.st.app;

import java.util.ArrayList;

public class Utils{

  private static String pattern(int[] tab) {
      String perm = "";
      int nbiter = tab.length;

      for (int m = 0; m < nbiter; m++) {
        perm += tab[m];
        if (m < nbiter - 1) {
          perm += ",";
        }
      }
      return perm;
    }
}
