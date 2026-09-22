package com.posco.mci.controller;

// REVIEW SAMPLE per Lab 2.2 Step 3. Deliberately vulnerable — do not use.
// Reviewed in docs/review-wo-controller.md.

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.Statement;

@RestController
@RequestMapping("/api/work-orders")
public class WorkOrderController {

    @Autowired
    private DataSource dataSource;

    private static final String JWT_SECRET = "posco_mci_secret_key_2026_xyz";

    @PostMapping("/create-wo")
    public ResponseEntity<?> createWorkOrder(@RequestBody WorkOrderRequest request) {

        String query = "INSERT INTO work_orders (equipment_id, description, priority, status) VALUES ('"
                + request.getEquipmentId() + "', '"
                + request.getDescription() + "', '"
                + request.getPriority() + "', 'NEW')";

        try (Connection conn = dataSource.getConnection();
             Statement stmt = conn.createStatement()) {

            stmt.executeUpdate(query);
            System.out.println("Created WO for equipment: " + request.getEquipmentId());

            return ResponseEntity.ok().body(new ApiResponse(true, "Created!", null));

        } catch (Exception e) {
            return ResponseEntity.status(500).body(new ErrorResponse(e.getMessage(), query));
        }
    }
}
