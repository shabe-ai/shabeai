"use client";
import dynamic from "next/dynamic";
const BillingPage = dynamic(() => import("./BillingPageImpl"), { ssr: false });
export default BillingPage; 