package com.example.cardetect;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {
    TextView nearestSlotTxt,totalSlotCountTxt,slotCountTxtA,slotCountTxtB,slotCountTxtC,slotCountTxtD;
    String nearestSlot,slotCountA,slotCountB,slotCountC,slotCountD;
    DatabaseReference databaseReference;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        nearestSlotTxt = findViewById(R.id.txtNearestSlot);
        totalSlotCountTxt = findViewById(R.id.txtTotalSlotCount);
        slotCountTxtA = findViewById(R.id.txtSlotCountA);
        slotCountTxtB = findViewById(R.id.txtSlotCountB);
        slotCountTxtC = findViewById(R.id.txtSlotCountC);
        slotCountTxtD = findViewById(R.id.txtSlotCountD);
        databaseReference = FirebaseDatabase.getInstance().getReference().child("AutoPark");
        refresh();

    }

    private void getSections(){
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                if(snapshot.exists()){
                    nearestSlotTxt.setText(snapshot.child("Main").child("nearestSlot").getValue().toString());
                    totalSlotCountTxt.setText(snapshot.child("Main").child("totalSlotCount").getValue().toString());
                    slotCountTxtA.setText(snapshot.child("SectionA").child("slotCount").getValue().toString());
                    slotCountTxtB.setText(snapshot.child("SectionB").child("slotCount").getValue().toString());
                    slotCountTxtC.setText(snapshot.child("SectionC").child("slotCount").getValue().toString());
                    slotCountTxtD.setText(snapshot.child("SectionD").child("slotCount").getValue().toString());
                }

            }
            @Override
            public void onCancelled(@NonNull DatabaseError error) {
            }
        });
    }

    int count = 0;
    public void refresh(){
        count++;
        getSections();
        content(1000);
    }

    private void content(int miliseconds) {
        final Handler handler = new Handler();
        final Runnable runnable = new Runnable() {
            @Override
            public void run() {
                refresh();
            }
        };
        handler.postDelayed(runnable,miliseconds);
    }

}